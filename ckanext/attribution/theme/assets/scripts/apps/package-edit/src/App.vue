<template>
    <div>
        <CitationPreview/>
        <div class="cited-contributors">
            <draggable v-model="citedContributors" group="citationOrder" handle=".citation-ordering">
                <ContributionBlock v-for="contributor in citedContributors" :contributor-id="contributor.id"
                                   :key="contributor.id"/>
            </draggable>
        </div>
        <div class="other-contributors">
            <draggable v-model="otherContributors" group="citationOrder" handle=".citation-ordering">
                <ContributionBlock v-for="contributor in otherContributors" :contributor-id="contributor.id"
                                   :key="contributor.id"/>
            </draggable>
        </div>
        <AgentSearch/>
        <input type="hidden" id="contributor-content" name="attribution" :value="serialisedContent">
    </div>
</template>

<script>
import ContributionBlock from './components/ContributionBlock.vue';
import AgentSearch from './components/AgentSearch.vue';
import {mapActions, mapMutations, mapGetters} from 'vuex';
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
    props     : ['packageId', 'canEdit'],
    data      : function () {
        return {
            sortedAgents: []
        };
    },
    computed  : {
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
        ...mapActions(['initialise', 'getPackage']),
        ...mapMutations(['setEditPermission'])
    },
    created   : function () {
        this.getPackage(this.packageId);
        this.setEditPermission(this.canEdit === 'True');
        this.initialise();
    }
};
</script>