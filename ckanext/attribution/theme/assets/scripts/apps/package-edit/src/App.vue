<template>
    <div>
        <CitationPreview/>
        <div class="cited-contributors" :class="{'attribution-loading': results.loading}">
            <draggable v-model="citedContributors" group="citationOrder" handle=".citation-ordering">
                <ContributionBlock v-for="contributor in citedContributors" :contributor-id="contributor.id"
                                   :key="contributor.id"/>
            </draggable>
        </div>
        <div class="other-contributors" :class="{'attribution-loading': results.loading}">
            <draggable v-model="otherContributors" group="citationOrder" handle=".citation-ordering">
                <ContributionBlock v-for="contributor in otherContributors" :contributor-id="contributor.id"
                                   :key="contributor.id"/>
            </draggable>
        </div>
        <div class="contributor-pagination" v-if="results.total > results.pageSize">
            <div>
                <span class="page-btn" v-if="results.offset - results.pageSize >= 0" @click="previousPage">
                    <i class="fas fa-arrow-left"></i>
                    Previous
                </span>
            </div>
            <div>
                <span v-if="!results.loading">{{results.offset + 1}} - {{results.offset + results.pageSize}}</span>
                <i v-if="results.loading" class="fas fa-spin fa-spinner"></i>
                <span style="padding-left: 0.4em;">of {{ results.total }} total contributors loaded</span>
                <help-tooltip>
                    To reduce page load times and make it easier to read the rest of the page, only {{ results.pageSize }} contributors are loaded at a time.
                </help-tooltip>
            </div>
            <div>
                <span class="page-btn" v-if="results.offset + results.pageSize < results.total" @click="nextPage">
                    Next
                    <i class="fas fa-arrow-right"></i>
                </span>
            </div>
        </div>
        <AgentSearch/>
        <input type="hidden" id="contributor-content" name="attribution" :value="serialisedContent">
    </div>
</template>

<script>
import ContributionBlock from './components/ContributionBlock.vue';
import AgentSearch from './components/AgentSearch.vue';
import {mapActions, mapMutations, mapGetters, mapState} from 'vuex';
import {Agent, Citation} from './models/main';
import draggable from 'vuedraggable';
const CitationPreview = import(/* webpackChunkName: 'citations' */ './components/CitationPreview.vue')
import Loader from './components/Loader.vue';

export default {
    name      : 'App',
    components: {
        CitationPreview: () => ({component: CitationPreview, loading: Loader}),
        ContributionBlock,
        AgentSearch,
        draggable
    },
    props     : ['packageId', 'canEdit', 'doiPlugin'],
    data      : function () {
        return {
            sortedAgents: []
        };
    },
    computed  : {
        ...mapState(['results']),
        ...mapGetters(['serialisedContent']),
        citedContributors: {
            get() {
                return Agent.query()
                            .with('meta')
                            .where('isActive', true)
                            .where('citeable', true)
                            .get()
                            .sort((a, b) => {
                                // .orderBy doesn't seem to update automatically but this does
                                return a.citation.order - b.citation.order;
                            });
            },
            set(newValue) {
                newValue.forEach((v, i) => {
                    let makeCitation = [];
                    if (!v.citation) {
                        makeCitation.push(Citation.insert({
                            data: {
                                activity: '[citation]',
                                scheme  : 'internal',
                                agent_id: v.id,
                                order   : i + 1,
                                meta    : {is_new: true}
                            }
                        }));
                    } else if (!v.citeable) {
                        makeCitation.push(Citation.updateMeta(v.citation.id, {to_delete: false}));
                    }

                    Promise.all(makeCitation).then(() => {
                        if (v.citation.order !== i + 1) {
                            Citation.update({where: v.citation.id, data: {order: i + 1}});
                            Citation.updateMeta(v.citation.id, {is_dirty: true})
                        }
                    });
                });
            }
        },
        otherContributors: {
            get() {
                return Agent.query()
                            .with('meta')
                            .where('isActive', true)
                            .where('citeable', false)
                            .orderBy('agent_type', 'desc')
                            .orderBy('standardisedName')
                            .get();
            },
            set(newValue) {
                newValue.forEach(v => {
                    if (v.citation) {
                        Citation.updateMeta(v.citation.id, {to_delete: true});
                    }
                });
            }
        }
    },
    methods   : {
        ...mapActions(['initialise', 'getPackage', 'nextPage', 'previousPage']),
        ...mapMutations(['updateSettings'])
    },
    created   : function () {
        this.updateSettings({
            packageId: this.packageId,
            canEdit: this.canEdit === 'True',
            doiPlugin: this.doiPlugin === 'True'
        })
        this.getPackage();
        this.initialise();
    }
};
</script>