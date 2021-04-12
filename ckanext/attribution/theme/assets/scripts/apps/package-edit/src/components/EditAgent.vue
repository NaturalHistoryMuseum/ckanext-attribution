<template>
    <div class="agent-edit-block agent-detail" :class="'agent-'+edits.agent_type.toLowerCase()">
        <div class="agent-header">
            <AgentTypeField v-model="edits.agent_type"/>
            <span class="display-name">
                <em>{{ displayName }}</em>
            </span>
            <div class="edit-icons">
                <span class="edit-icon" title="Download contributor details from external source"
                      v-if="contributor.external_id" @click="syncAgent">
                    <i class="fas"
                       :class="contributor.meta.syncing ? 'fa-spinner fa-spin' : 'fa-arrow-alt-circle-down'"></i>
                </span>
                <span class="edit-icon" title="Edit" v-if="canEdit" @click="$emit('toggle-edit')">
                    <i class="fas fa-edit"></i>
                </span>
                <span class="edit-icon" title="Remove this contributor"
                      @click="eventBus.$emit(events.removeContributor, contributorId)">
                    <i class="fas fa-minus-circle"></i>
                </span>
            </div>
        </div>
        <div class="agent-id-edit attribution-row">
            <select-field v-model="edits.external_id_scheme" :options="Object.entries(controlledLists.agentIdSchemes)"
                          :opt-label="o => o[1].label" :opt-value="o => o[0]" :class="['wrap-small']">
                External ID scheme
            </select-field>
            <text-field v-model="edits.external_id"
                        :placeholder="controlledLists.agentIdSchemes[edits.external_id_scheme].label"
                        :class="['wrap-small']">
                <i :class="controlledLists.agentIdSchemes[edits.external_id_scheme].fa_icon"></i>
                {{ controlledLists.agentIdSchemes[edits.external_id_scheme].label }}
            </text-field>
        </div>
        <div class="expand-bar" title="Expand" @click="expand = !expand">
            <small>Show all edit options</small>
            <i class="fas" :class="expand ? 'fa-caret-up' : 'fa-caret-down'"></i>
        </div>
        <template v-if="expand">
            <div class="agent-name-edit attribution-row">
                <template v-if="edits.agent_type === 'person'">
                    <text-field v-model="edits.family_name" :cls="['wrap-small']">
                        Family name
                    </text-field>
                    <text-field v-model="edits.given_names" :cls="['wrap-small']">
                        Given name(s)
                    </text-field>
                    <div class="attribution-field one-line" v-for="fieldId in idGen">
                        <label :for="fieldId">
                            Given names first
                        </label>
                        <input :id="fieldId" type="checkbox" v-model="edits.given_names_first">
                    </div>
                    <help-tooltip>
                        Does this person's culture or language typically place given or family
                        names first? (this does not affect sorting)
                    </help-tooltip>
                </template>
                <template v-if="edits.agent_type !== 'person'">
                    <text-field v-model="edits.name">
                        Name
                    </text-field>
                    <text-field v-model="edits.location">
                        Location
                    </text-field>
                </template>
            </div>
            <div class="agent-user-edit attribution-row">
                <autocomplete-field v-model="edits.user_id" @typing="updateUserOptions" :options="userOptions"
                                    label="Associated user" :item-id="'agent-user-' + contributorId">
                </autocomplete-field>
                <help-tooltip>
                    If this contributor has a user account registered on the portal, associate it here
                </help-tooltip>
            </div>
            <div class="agent-affiliations-edit attribution-row">
                <autocomplete-list v-model="affiliations" @typing="updateAffiliationOptions"
                                   :options="affiliationOptions"
                                   label="Add affiliation" :item-id="'agent-affiliation-' + contributorId">
                </autocomplete-list>
                <help-tooltip>
                    <!-- TODO: make agent edit page and add link here -->
                    For affiliations that are associated with <em>this package only</em>. Only includes contributors
                    that have already been added to this page.
                </help-tooltip>
            </div>
        </template>
        <div class="attribution-save">
            <span class="btn btn-primary" @click="saveChanges">
                <i class="fas fa-save"></i>
                Save changes
            </span>
            <span class="btn btn-primary" @click="$emit('toggle-edit')">
                <i class="fas fa-times"></i>
                Cancel
            </span>
        </div>
    </div>
</template>

<script>
import {mapActions, mapState} from 'vuex';
import {get} from '../api';
import {nanoid} from 'nanoid';
import Common from './Common.vue';
import {Affiliation, Agent} from '../models/main';
import AgentTypeField from './fields/AgentTypeField.vue';

export default {
    name      : 'EditAgent',
    extends   : Common,
    components: {
        AgentTypeField
    },
    data      : function () {
        return {
            edits             : {},
            affiliations      : [],
            expand            : false,
            userOptions       : [],
            affiliationOptions: [],
            syncing           : false
        };
    },
    computed  : {
        ...mapState(['canEdit', 'packageId', 'controlledLists']),
        contributor() {
            return Agent.query()
                        .with('meta')
                        .with('affiliations.other_agent')
                        .with('affiliations.meta')
                        .find(this.contributorId);
        },
        displayName() {
            if (this.edits.agent_type !== 'person') {
                return this.edits.name;
            }
            if (this.edits.given_names_first) {
                return [this.edits.given_names, this.edits.family_name].join(' ');
            } else {
                return [this.edits.family_name, this.edits.given_names].join(' ');
            }
        },
        idGen() {
            return [nanoid(8)];
        }
    },
    methods   : {
        ...mapActions(['removeContributor']),
        saveChanges() {
            let promises = [];

            // add new affiliations
            let newAffiliations = this.affiliations.filter((a) => {
                return this.contributor.affiliations.findIndex(e => e.other_agent_id === a.value) === -1;
            }).map(a => {
                let body = {
                    agent_id      : this.contributorId,
                    other_agent_id: a.value,
                    package_id    : this.packageId,
                    meta          : {
                        is_new: true
                    }
                };

                if (!Agent.query().where('id', a.value).exists()) {
                    a.record.meta = {'is_new': true};
                    promises.push(Agent.insert({data: a.record}));
                }

                return body;
            });
            promises.push(Affiliation.insert({data: newAffiliations}));

            // mark any deleted ones as 'to_delete'
            this.contributor.affiliations.filter((a) => {
                return this.affiliations.findIndex(e => e.value === a.other_agent_id) === -1;
            }).forEach(a => {
                promises.push(Affiliation.updateMeta(a.id, {'to_delete': true}));
            });

            promises.push(Agent.update({
                where: this.contributorId,
                data : this.edits
            }));

            return Promise.all(promises).then(() => {
                return Agent.updateMeta(this.contributorId, {is_dirty: true});
            }).then(() => {
                    this.$emit('toggle-edit');
                }
            ).catch(e => console.error(e));
        },
        updateUserOptions(input) {
            if (input === '' || input === null) {
                this.userOptions = [];
                return;
            }
            get('user_list?q=' + input).then(users => {
                    this.userOptions = users.map(user => {
                        return {label: user.display_name, value: user.id};
                    });
                }
            );
        },
        updateAffiliationOptions: function (input) {
            let q = Agent.query()
                         .where('isActive', true)
                         .where(a => a.id !== this.contributorId)
                         .where(a => this.affiliations.findIndex(v => v.value === a.id) === -1);
            if (input && input !== '') {
                q = q.where(a => {
                    let inpt = input.toLowerCase();
                    let matchFamily = a.family_name ? a.family_name.toLowerCase()
                                                       .startsWith(inpt) : false;
                    let matchGiven = a.given_names ? a.given_names.toLowerCase()
                                                      .startsWith(inpt) : false;
                    let matchName = a.name ? a.name.toLowerCase().startsWith(inpt) : false;
                    return matchFamily || matchGiven || matchName;
                });
            }
            this.affiliationOptions = q.get().map(opt => {
                return {
                    label : opt.displayName,
                    value : opt.id,
                    record: opt
                };
            });
        },
        syncAgent() {
            this.$store.dispatch('syncAgent', this.contributorId).then(this.refresh);
        },
        refresh() {
            this.edits = this.contributor.getCopy();
            this.affiliations = this.contributor.affiliations.filter(a => !a.meta.to_delete).map(a => {
                return {label: a.other_agent.displayName, value: a.other_agent_id, record: a.other_agent};
            });
            // set some defaults
            if ((!this.edits.agent_type) && (!this.edits.external_id_scheme)) {
                this.$set(this.edits, 'agent_type', Object.keys(this.controlledLists.agentTypes)[0]);
            }
            if ((!this.edits.agent_type) && this.edits.external_id_scheme) {
                let hasAsDefault = Object.entries(this.controlledLists.agentTypes)
                                         .filter(t => t[1].default === this.edits.external_id_scheme);
                if (hasAsDefault.length > 0) {
                    this.$set(this.edits, 'agent_type', hasAsDefault[0][0]);
                }
            }
            if (!this.edits.external_id_scheme) {
                this.$set(this.edits, 'external_id_scheme',
                    this.controlledLists.agentTypes[this.edits.agent_type].default_scheme);
            }
            if (this.edits.given_names_first === undefined) {
                // TODO: do i need this?
                this.$set(this.edits, 'given_names_first', true);
            }

            // get user info
            if (this.edits.user_id) {
                get('user_show?id=' + this.edits.user_id).then(d => {
                    this.userOptions = [{label: d.display_name, value: this.edits.user_id}];
                });
            }
        }
    },
    created   : function () {
        this.refresh();
    }
};
</script>