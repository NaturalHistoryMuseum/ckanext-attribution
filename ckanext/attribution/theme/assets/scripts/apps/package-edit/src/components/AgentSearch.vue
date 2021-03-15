<template>
    <div class="contribution-block-new">
        <div class="new-contribution-header">
            <span>
                <b>Search by name or ID:</b>
            </span>
            <div class="toggle-wrapper">
                <span class="toggle-label">Include external results:</span>
                <input id="external-search-toggle" v-model="useExternalSearch" type="checkbox" class="toggle-switch"
                       @change="redoSearch">
                <label for="external-search-toggle"></label>
                <div class="help-icon">
                    <i class="fas fa-question-circle"></i>
                    <div class="help-tooltip" role="tooltip">
                        Search external APIs (e.g. ORCID and ROR) for contributors that have not yet
                        been imported. This may take several seconds.
                    </div>
                </div>
            </div>

            <autocomplete-field v-model="newAgent" @typing="updateAgentOptions" :options="agentOptions"
                                item-id="new-agent" :delay="1000" :loading="searchLoading" :failed="searchFailed">
                <div class="autocomplete-option null-option" @click="$emit('custom-option', {label: null, value: {}})">
                    manual add
                </div>
            </autocomplete-field>
        </div>
        <NewAgent :details="newAgent" v-if="newAgent" :affiliations="[]" v-on:toggle-edit="newAgent = null"/>
    </div>
</template>

<script>
import {mapGetters} from 'vuex';
import {get} from '../api';
import NewAgent from './NewAgent.vue';
import Agent from './Agent.vue';
import axios from 'axios';

export default {
    name: 'AgentSearch',
    components: {NewAgent, Agent},
    data: function () {
        return {
            newAgent: null,
            agentOptions: {},
            optionSearchInput: null,
            searchFailed: null,
            useExternalSearch: false,
            queuedSearches: 0  // handles cancelled/overwritten requests
        }
    },
    computed: {
        ...mapGetters(['agents', 'identifierType']),
        searchLoading() {
            return this.queuedSearches > 0;
        }
    },
    methods: {
        updateAgentOptions(input) {
            if (input === '' || input === null) {
                this.agentOptions = [];
                return;
            }
            if (input === this.optionSearchInput) {
                return;
            }
            this.optionSearchInput = input;
            this.agentOptions = {}

            this.searchFailed = null;
            this.queuedSearches++;
            get('agent_list?q=' + input, 'internalSearch').then(d => {
                    this.$set(this.agentOptions, 'default', d.result.map(agent => {
                        return {label: agent.display_name, value: agent}
                    }).filter(opt => {
                        return !Object.keys(this.agents).includes(opt.value.id);
                    }))
                }
            ).catch(e => {
                if (!axios.isCancel(e)) {
                    this.searchFailed = e;
                }
            }).finally(() => {
                this.queuedSearches--;
            })

            if (this.useExternalSearch) {
                this.queuedSearches++;
                get('agent_external_search?q=' + input, 'externalSearch').then(d => {
                    if (!d.success) {
                        return;
                    }
                    Object.entries(d.result).forEach(source => {
                        let idType = this.identifierType(source[0]);
                        this.$set(this.agentOptions, idType.details.label, source[1].records.map(agent => {
                            let label = agent.name;
                            if (agent.family_name) {
                                label = agent.family_name + ', ' + agent.given_names
                            }
                            return {
                                label: label,
                                value: agent
                            }
                        }))
                    })
                }).catch(e => {
                    if (!axios.isCancel(e)) {
                        this.searchFailed = e;
                    }
                }).finally(() => {
                    this.queuedSearches--;
                })
            }
        },
        redoSearch() {
            let input = this.optionSearchInput;
            this.optionSearchInput = null;
            this.updateAgentOptions(input);
        }
    }
}
</script>