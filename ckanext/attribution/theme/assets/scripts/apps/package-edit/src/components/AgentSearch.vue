<template>
    <div class="contribution-block-new">
        <div class="new-contribution-search">
            <label for="autocomplete-text-new-agent">
                Add new contributor
            </label>
            <div class="checkboxes">
                <template v-for="source in external">
                    <input type="checkbox" v-model="source.enabled" :id="`${source.name}-chk`" @change="redoSearch">
                    <label :for="`${source.name}-chk`" :title="`Include results from ${source.label}`">{{
                            source.label
                        }}</label>
                </template>
                <div class="help-icon">
                    <i class="fas fa-question-circle"></i>
                    <div class="help-tooltip" role="tooltip" id="orcid-search-toggle-help">
                        Search external sources for contributors that have not yet been imported.
                        This may take several seconds.
                    </div>
                </div>
            </div>
            <autocomplete-field v-model="selectedAgent" @typing="updateSearchResults" @input="setAgent"
                                :options="searchResults" @cancel="cancelSearches"
                                item-id="new-agent" :delay="1000" :loading="searchLoading" :failed="searchFailed">
                No results found; try adding manually (below)
            </autocomplete-field>
        </div>
        <div class="new-contribution-manual">
            <span @click="setAgent({})">or add manually</span>
            <i class="fas fa-pencil-alt"></i>
        </div>
        <ShowAgent :contributor-id="newAgentId" v-if="newAgent && !newAgent.meta.is_editing"/>
        <EditAgent :contributor-id="newAgentId" v-if="newAgent && newAgent.meta.is_editing"
                   @validated="e => valid.agent = e"/>
        <EditActivity :activity-id="activity.id" v-if="activity"
                      @validated="e => valid.activity = e"/>
        <div class="attribution-save" v-if="newAgentId">
            <span class="btn" :class="valid.agent && valid.activity ? 'btn-primary' : 'btn-disabled'" @click="saveChanges">
                <i class="fas fa-save"></i>
                Add
            </span>
            <span class="btn btn-primary" @click="cancelChanges">
                <i class="fas fa-times"></i>
                Cancel
            </span>
        </div>
    </div>
</template>

<script>
import {mapActions, mapState} from 'vuex';
import {cancelAll, get} from '../api';
import axios from 'axios';
import {Activity, Agent, Citation} from '../models/main';
import {eventBus, events} from '../eventbus';

const ShowAgent = () => import(/* webpackChunkName: 'show-agent' */ './ShowAgent.vue');
const EditAgent = () => import(/* webpackChunkName: 'edit-agent' */ './EditAgent.vue');
const EditActivity = () => import(/* webpackChunkName: 'edit-activity' */ './EditActivity.vue');

export default {
    name      : 'AgentSearch',
    components: {EditAgent, EditActivity, ShowAgent},
    data      : function () {
        return {
            selectedAgent : null,  // result from the search box
            newAgentId    : null,  // agent currently being edited
            searchResults : {},
            searchString  : null,
            searchFailed  : null,
            external      : [
                {
                    name   : 'orcid',
                    label  : 'ORCID',
                    enabled: false
                },
                {
                    name   : 'ror',
                    label  : 'ROR',
                    enabled: false
                }
            ],
            queuedSearches: 0,  // handles cancelled/overwritten requests
            valid         : {
                agent   : false,
                activity: false
            }
        };
    },
    computed  : {
        ...mapState(['controlledLists', 'packageId']),
        searchLoading() {
            return this.queuedSearches > 0;
        },
        activity() {
            if (this.newAgent && this.newAgent.activities) {
                return this.newAgent.activities.slice(-1)[0];
            } else {
                return null;
            }
        },
        useExternalSearch() {
            return this.external.some(x => x.enabled);
        },
        newAgent() {
            if (this.newAgentId) {
                return Agent.query().with('meta').find(this.newAgentId);
            }
        },
    },
    methods   : {
        ...mapActions(['purgeTemporary']),
        cancelSearches() {
            cancelAll();
            this.searchFailed = new Error('Search cancelled.');
        },
        updateSearchResults(input) {
            if (input === '' || input === null) {
                this.searchString = null;
                this.searchResults = [];
                return;
            }
            if (input === this.searchString) {
                return;
            }
            this.searchString = input;
            this.searchResults = {};

            this.searchFailed = null;
            this.queuedSearches++;
            get('agent_list', {q: input}, 'internalSearch').then(agents => {
                    this.$set(this.searchResults, 'default', agents.map(agent => {
                        let label = agent.display_name;
                        if (agent.external_id) {
                            label += ` (${agent.external_id})`;
                        }
                        return {
                            label: label,
                            value: agent
                        };
                    }).filter(opt => {
                        return !Agent.query()
                                     .whereHas('meta', q => {
                                         q.where('is_hidden', false);
                                     })
                                     .where('id', opt.value.id).exists();
                    }));
                }
            ).catch(e => {
                if (!axios.isCancel(e)) {
                    cancelAll();
                    this.searchFailed = e;
                }
            }).finally(() => {
                this.queuedSearches--;
            });

            if (this.useExternalSearch) {
                this.queuedSearches++;
                let sources = this.external.filter(x => x.enabled).map(x => x.name);
                get('agent_external_search', {q: input, sources: sources}, 'externalSearch').then(agents => {
                    if (!agents) {
                        return;
                    }
                    Object.entries(agents).forEach(source => {
                        let idType = this.controlledLists.agentIdSchemes[source[0]];
                        this.$set(this.searchResults, idType.label, source[1].records.map(agent => {
                            let label = agent.name;
                            if (agent.family_name) {
                                label = agent.family_name + ', ' + agent.given_names;
                            }
                            return {
                                label: label,
                                value: agent
                            };
                        }));
                    });
                }).catch(e => {
                    if (!axios.isCancel(e)) {
                        cancelAll();
                        this.searchFailed = e;
                    }
                }).finally(() => {
                    this.queuedSearches--;
                });
            }
        },
        redoSearch() {
            let input = this.searchString;
            this.searchString = null;
            this.updateSearchResults(input);
        },
        saveChanges() {
            eventBus.$emit(events.saveAgent, this.newAgentId);
            eventBus.$emit(events.saveActivity, this.activity.id);
            Agent.updateMeta(this.newAgentId, {is_hidden: false, is_temporary: false});
            Activity.updateMeta(this.activity.id, {is_hidden: false, is_temporary: false})
            this.selectedAgent = null;
            this.newAgentId = null;
            this.searchString = null;
        },
        cancelChanges() {
            this.purgeTemporary();
            this.selectedAgent = null;
            this.newAgentId = null;
            this.searchString = null;
        },
        setAgent(input) {
            if (!input) {
                this.selectedAgent = null;
                return;
            }
            let alreadyImported = null;
            let newId = null;
            if (input.id) {
                alreadyImported = Agent.query().where('id', input.id).get();
            } else if (input.external_id) {
                alreadyImported = Agent.query()
                                       .where('external_id', input.external_id)
                                       .where('external_id_scheme', input.external_id_scheme)
                                       .get();
            }

            let updateAgent;
            if (alreadyImported && alreadyImported.length > 0) {
                newId = alreadyImported[0].id;
                updateAgent = () => Agent.updateMeta(newId, {is_hidden: true, to_delete: false, is_new: true});
            } else {
                input.meta = {
                    is_hidden   : true,
                    to_delete   : false,
                    is_new      : true,
                    is_editing  : Object.keys(input).length === 0,
                    is_temporary: true
                };
                updateAgent = () => Agent.insert({data: input}).then(records => {
                    newId = records.agents[0].id;
                });
            }

            updateAgent().then(() => {
                Activity.insert({
                    data:
                        {
                            agent_id  : newId,
                            package_id: this.packageId,
                            meta      : {is_new: true, is_editing: true, is_temporary: true}
                        }
                }).then(() => {
                    let citationCount = Agent.query()
                                             .where('isActive', true)
                                             .where('citeable', true)
                                             .count();
                    return Citation.insert({
                        data: {
                            agent_id  : newId,
                            package_id: this.packageId,
                            order     : citationCount + 1,
                            meta      : {is_new: true}
                        }
                    });
                }).then(() => {
                    this.newAgentId = newId;
                });
            });
        }
    }
};
</script>