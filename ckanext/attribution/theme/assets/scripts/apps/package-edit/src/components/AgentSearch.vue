<template>
    <div class="contribution-block-new">
        <div class="new-contribution-header">
            <label for="autocomplete-text-new-agent">
                Add new contributor:
            </label>
            <div class="toggle-wrapper">
                <span class="toggle-label">Include external results?</span>
                <input id="external-search-toggle" v-model="useExternalSearch" type="checkbox" class="toggle-switch"
                       @change="redoSearch" aria-labelledby="external-search-toggle-help">
                <label for="external-search-toggle">
                    <span class="screenreader">Enable/disable searching external services</span>
                </label>
                <div class="help-icon">
                    <i class="fas fa-question-circle"></i>
                    <div class="help-tooltip" role="tooltip" id="external-search-toggle-help">
                        Search external APIs (e.g. ORCID and ROR) for contributors that have not yet
                        been imported. This may take several seconds.
                    </div>
                </div>
            </div>

            <autocomplete-field v-model="newAgent" @typing="updateAgentOptions" @input="setAgent"
                                :options="agentOptions"
                                item-id="new-agent" :delay="1000" :loading="searchLoading" :failed="searchFailed">
            </autocomplete-field>
        </div>
        <ShowAgent :contributor-id="newAgent.id" v-if="newAgent && newAgent.id"/>
        <EditActivity :activity-id="activity.id" v-if="activity" v-on:toggle-edit="finish"/>
    </div>
</template>

<script>
import {mapState} from 'vuex';
import {cancelAll, get} from '../api';
const ShowAgent = () => import(/* webpackChunkName: 'show-agent' */ './ShowAgent.vue');
import axios from 'axios';
import {Activity, Agent, Citation} from '../models/main';
const EditActivity = () => import(/* webpackChunkName: 'edit-activity' */ './EditActivity.vue');

export default {
    name      : 'AgentSearch',
    components: {EditActivity, ShowAgent},
    data      : function () {
        return {
            newAgent         : null,
            agentOptions     : {},
            optionSearchInput: null,
            searchFailed     : null,
            useExternalSearch: false,
            queuedSearches   : 0  // handles cancelled/overwritten requests
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
        }
    },
    methods   : {
        updateAgentOptions(input) {
            if (input === '' || input === null) {
                this.optionSearchInput = null;
                this.agentOptions = [];
                return;
            }
            if (input === this.optionSearchInput) {
                return;
            }
            this.optionSearchInput = input;
            this.agentOptions = {};

            this.searchFailed = null;
            this.queuedSearches++;
            get('agent_list?q=' + input, 'internalSearch').then(agents => {
                    this.$set(this.agentOptions, 'default', agents.map(agent => {
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
                get('agent_external_search?q=' + input, 'externalSearch').then(agents => {
                    if (!agents) {
                        return;
                    }
                    Object.entries(agents).forEach(source => {
                        let idType = this.controlledLists.agentIdSchemes[source[0]];
                        this.$set(this.agentOptions, idType.label, source[1].records.map(agent => {
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
            let input = this.optionSearchInput;
            this.optionSearchInput = null;
            this.updateAgentOptions(input);
        },
        finish() {
            Agent.updateMeta(this.newAgent.id, {'is_hidden': false});
            this.newAgent = null;
            this.optionSearchInput = null;
        },
        setAgent(input) {
            if (!input) {
                this.newAgent = null;
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
                input.meta = {is_hidden: true, to_delete: false, is_new: true};
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
                            meta      : {is_new: true, is_editing: true}
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
                    this.newAgent = Agent.find(newId);
                });
            });
        }
    }
};
</script>