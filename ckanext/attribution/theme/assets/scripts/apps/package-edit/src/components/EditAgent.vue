<template>
    <div class="agent-edit-block agent-detail" :class="'agent-'+editedDetails.agent_type.toLowerCase()">
        <div class="agent-header">
            <div class="agent-type-edit">
                <span v-for="(iconName, agentType) in iconDict" class="agent-type-option">
                    <input type="radio" :value="agentType" v-model="editedDetails.agent_type"
                           :id="'agent-type-option-' + agentType + details.id">
                    <label :for="'agent-type-option-' + agentType + details.id">
                        <i class="fas" :class="'fa-' + iconName"></i>
                    </label>
                </span>
            </div>
            <span class="display-name">
                <em>{{ displayName }}</em>
            </span>
            <div class="edit-icons">
                <span class="edit-icon" title="Download details from external source"
                      v-if="editedDetails.external_id" @click="updateFromExternal">
                    <i class="fas" :class="syncing ? 'fa-spinner fa-spin' : 'fa-arrow-alt-circle-down'"></i>
                </span>
                <span class="edit-icon" title="Remove this contributor" @click="removeAgent(details.id)">
                    <i class="fas fa-minus-circle"></i>
                </span>
            </div>
        </div>
        <div class="agent-id-edit attribution-row">
            <select-field v-model="editedDetails.external_id_scheme" :options="schemeDict"
                          :opt-label="o => o.details.label" :opt-value="o => o.name" :class="['wrap-small']">
                External ID scheme
            </select-field>
            <text-field v-model="editedDetails.external_id" :placeholder="editedDetails.external_id_scheme"
                        :class="['wrap-small']">
                <i :class="identifierIcon(editedDetails.external_id_scheme)"></i>
                {{ identifierType(editedDetails.external_id_scheme).details.label }}
            </text-field>
        </div>
        <div class="expand-bar" title="Show all edit options" @click="expand = !expand">
            <i class="fas" :class="expand ? 'fa-caret-up' : 'fa-caret-down'"></i>
        </div>
        <template v-if="expand">
            <div class="agent-name-edit attribution-row">
                <template v-if="editedDetails.agent_type === 'individual'">
                    <text-field v-model="editedDetails.family_name" :cls="['wrap-small']">
                        Family name
                    </text-field>
                    <text-field v-model="editedDetails.given_names" :cls="['wrap-small']">
                        Given name(s)
                    </text-field>
                    <div class="attribution-field one-line" v-for="fieldId in idGen">
                        <label :for="fieldId">
                            Given names first
                        </label>
                        <input :id="fieldId" type="checkbox" v-model="editedDetails.given_names_first">
                    </div>
                    <help-tooltip>
                        Does this person's culture typically place given or family names first? (this
                        does not affect sorting)
                    </help-tooltip>
                </template>
                <template v-if="editedDetails.agent_type !== 'individual'">
                    <text-field v-model="editedDetails.name" :oneline="true">
                        Name
                    </text-field>
                </template>
            </div>
            <div class="agent-user-edit attribution-row">
                <autocomplete-field v-model="editedDetails.user_id" @typing="updateUserOptions" :options="userOptions"
                                    label="Associated user" :item-id="'agent-user-' + details.id">
                </autocomplete-field>
                <help-tooltip>
                    If this contributor has a user account registered on the portal, associate it here
                </help-tooltip>
            </div>
            <div class="agent-affiliations-edit attribution-row">
                <autocomplete-list v-model="editedDetails.affiliations" @typing="updateAffiliationOptions"
                                   :options="affiliationOptions"
                                   label="Add affiliation" :item-id="'agent-affiliation-' + details.id">
                </autocomplete-list>
                <help-tooltip>
                    <!-- TODO: make agent edit page and add link here -->
                    For affiliations that are associated with <em>this package only</em>.
                </help-tooltip>
            </div>
        </template>
        <div class="agent-save">
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
import {mapActions, mapGetters, mapState} from 'vuex';
import _ from 'lodash';
import {get, post} from '../api';
import {nanoid} from 'nanoid';

export default {
    name: 'EditAgent',
    props: ['details', 'affiliations'],
    components: {},
    data: function () {
        return {
            editedDetails: {},
            expand: false,
            userOptions: [],
            affiliationOptions: [],
            syncing: false
        }
    },
    computed: {
        ...mapState(['canEdit', 'iconDict', 'packageId', 'schemeDict']),
        ...mapGetters(['identifierIcon', 'defaultIdentifierType', 'identifierType']),
        displayName() {
            if (this.editedDetails.agent_type !== 'individual') {
                return this.editedDetails.name;
            }
            if (this.editedDetails.given_names_first) {
                return [this.editedDetails.given_names, this.editedDetails.family_name].join(' ');
            } else {
                return [this.editedDetails.family_name, this.editedDetails.given_names].join(' ');
            }
        },
        idGen() {
            return [nanoid(8)]
        }
    },
    methods: {
        ...mapActions(['externalUpdate', 'removeAgent']),
        saveChanges() {
            // double check the id
            this.editedDetails.id = this.details.id;

            post('agent_update', this.editedDetails).catch((e) => {
                console.error(e)
            });
            let currentAffiliationIds = this.affiliations.map((a) => a.agent.id);
            let editedAffiliationIds = this.editedDetails.affiliations.map((a) => a.value);
            let newAffiliations = editedAffiliationIds.filter((a) => {
                return !currentAffiliationIds.includes(a);
            })
            newAffiliations.forEach((a) => {
                let body = {
                    agent_a_id: this.details.id,
                    agent_b_id: a,
                    package_id: this.packageId
                }
                post('agent_affiliation_create', body).catch((e) => {
                    console.error(e);
                });
            })
            let deletedAffiliations = this.affiliations.filter((a) => {
                return !editedAffiliationIds.includes(a.agent.id);
            })
            deletedAffiliations.forEach((a) => {
                let body = {
                    id: a.affiliation.id
                }
                post('agent_affiliation_delete', body).catch((e) => {
                    console.error(e);
                });
            })
            this.$emit('toggle-edit');
        },
        updateUserOptions(input) {
            if (input === '' || input === null) {
                this.userOptions = [];
                return;
            }
            get('user_list?q=' + input).then(d => {
                    this.userOptions = d.result.map(user => {
                        return {label: user.display_name, value: user.id}
                    })
                }
            ).catch(e => {
                console.error(e);
            })
        },
        updateAffiliationOptions(input) {
            if (input === '' || input === null) {
                this.affiliationOptions = [];
                return;
            }
            get('agent_list?q=' + input).then(d => {
                    this.affiliationOptions = d.result.map(agent => {
                        return {label: agent.display_name, value: agent.id}
                    }).filter(opt => {
                        let notSelf = opt.value !== this.details.id;
                        let notAdded = this.editedDetails.affiliations.filter(a => a.value === opt.value).length === 0;
                        return notSelf && notAdded;
                    })
                }
            ).catch(e => {
                console.error(e);
            })
        },
        resetEdits() {
            this.editedDetails = _.cloneDeep(this.details);
            // set some defaults
            if ((!this.editedDetails.agent_type) && (!this.editedDetails.external_id_scheme)) {
                // TODO: probably need a more centralised list of agent types (i.e. via API)
                this.$set(this.editedDetails, 'agent_type', Object.keys(this.iconDict)[0])
            }
            if ((!this.editedDetails.agent_type) && this.editedDetails.external_id_scheme) {
                this.$set(this.editedDetails, 'agent_type',
                    this.identifierType(this.editedDetails.external_id_scheme).details.default[0])
            }
            if (!this.editedDetails.external_id_scheme) {
                this.$set(this.editedDetails, 'external_id_scheme',
                    this.defaultIdentifierType(this.editedDetails.agent_type).name)
            }
            if (this.editedDetails.given_names_first === undefined) {
                this.$set(this.editedDetails, 'given_names_first', true);
            }

            // get user info
            if (this.editedDetails.user_id) {
                get('user_show?id=' + this.editedDetails.user_id).then(d => {
                    this.userOptions = [{label: d.result.display_name, value: this.editedDetails.user_id}]
                })
            }

            // get affiliation info
            this.$set(this.editedDetails, 'affiliations', this.affiliations.map(a => {
                return {label: a.agent.display_name, value: a.agent.id}
            }));
        },
        updateFromExternal() {
            this.syncing = true;
            let body = {id: this.details.id, external_id: this.editedDetails.external_id}

            post('agent_update', body).then(() => {
                return this.externalUpdate(this.details.id).then(() => {
                    this.$emit('toggle-edit');
                })
            }).catch(e => console.error(e)).finally(() => {
                this.syncing = false;
            });

        }
    },
    created: function () {
        this.resetEdits();
    }
}
</script>