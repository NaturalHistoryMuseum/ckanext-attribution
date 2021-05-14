import Vue from 'vue';
import Vuex from 'vuex';
import {get} from '../api';
import {Activity, Affiliation, Agent, Citation, Meta} from '../models/main';
import VuexORM from '@vuex-orm/core';

Vue.use(Vuex);

const database = new VuexORM.Database();
database.register(Agent);
database.register(Affiliation);
database.register(Activity);
database.register(Meta);
database.register(Citation);

const store = new Vuex.Store(
    {
        plugins  : [VuexORM.install(database)],
        state    : {
            settings: {
                packageId      : null,
                canEdit        : false,
                doiPlugin      : false,
            },
            packageDetail  : {},
            controlledLists: {
                'agentTypes'    : {},
                'activityTypes' : {},
                'activityLevels': [],
                'agentIdSchemes': {}
            }
        },
        getters  : {
            agentTypeIcon    : (state) => (agentType) => {
                let typeDetails = state.controlledLists.agentTypes[agentType];
                return typeDetails ? typeDetails.fa_icon : 'fas fa-asterisk';
            },
            agentIdIcon      : (state) => (idScheme) => {
                let schemeDetails = state.controlledLists.agentIdSchemes[idScheme];
                return schemeDetails ? schemeDetails.fa_icon : 'fas fa-link';
            },
            serialisedContent: () => {
                let serialise = (model) => model.query().with('meta').all().map(x => x.$toJson());
                return JSON.stringify({
                    agents      : serialise(Agent),
                    activities  : serialise(Activity),
                    affiliations: serialise(Affiliation),
                    citations   : serialise(Citation)
                });
            }
        },
        mutations: {
            updateSettings(state, payload) {
                Vue.set(state.settings, 'packageId', payload.packageId);
                Vue.set(state.settings, 'canEdit', payload.canEdit);
                Vue.set(state.settings, 'doiPlugin', payload.doiPlugin)
            }
        },
        actions  : {
            initialise(context) {
                return context.dispatch('initLists')
                              .then(() => context.dispatch('getContributions'));
            },
            getContributions(context) {
                if ((!context.state.settings.packageId) || context.state.settings.packageId === '') {
                    return;
                }
                return get('package_contributions_show', {id: context.state.settings.packageId})
                    .then(res => {
                        if (res === undefined) {
                            return;
                        }
                        let agentIds = res.map(r => r.agent.id);
                        // there seems to be some kind of bug in .create() where it will sometimes
                        // create everything and then delete it - manually clearing first then
                        // using .insert() instead avoids that
                        context.dispatch('entities/deleteAll').then(() => {
                            Agent.insert({
                                data: res.map(r => {
                                    let agent = r.agent;
                                    agent.affiliations = r.affiliations.map(a => {
                                        a.db_id = a.id;
                                        a.id = null;
                                        if (!agentIds.includes(a.other_agent.id)) {
                                            a.other_agent.meta = {is_hidden: true};
                                        }
                                        return a;
                                    });
                                    agent._activities = r.activities.filter(a => a.activity !== '[citation]')
                                                         .map(a => {
                                                             if (!a.package_id) {
                                                                 a.package_id = context.state.settings.packageId;
                                                             }
                                                             return a;
                                                         });
                                    agent._citation = r.activities.filter(a => a.activity === '[citation]')
                                                       .map(a => {
                                                           if (!a.package_id) {
                                                               a.package_id = context.state.settings.packageId;
                                                           }
                                                           return a;
                                                       })
                                                       .slice(-1)[0];
                                    return agent;
                                })
                            });
                        });
                    });
            },
            getPackage(context) {
                if ((!context.state.settings.packageId) || context.state.settings.packageId === '') {
                    return;
                }
                return get('package_show', {id: context.state.settings.packageId}).then(res => {
                    context.state.packageDetail = res;
                });
            },
            initLists(context) {
                return get('attribution_controlled_lists').then(res => {
                    Vue.set(context.state.controlledLists, 'agentTypes', res.agent_types);
                    Vue.set(context.state.controlledLists, 'activityTypes', res.contribution_activity_types);
                    Vue.set(context.state.controlledLists, 'activityLevels', res.contribution_activity_levels);
                    Vue.set(context.state.controlledLists, 'agentIdSchemes', res.agent_external_id_schemes);
                });
            },
            removeContributor(context, contributorId) {
                // mark for deletion rather than deleting instantly
                Agent.updateMeta(contributorId, {is_hidden: true, to_delete: true});
                Agent.query().with('_activities').find(contributorId).activities.forEach(a => {
                    Activity.updateMeta(a.id, {to_delete: true});
                });
            },
            syncAgent(context, contributorId) {
                // download details from external source
                Agent.updateMeta(contributorId, {syncing: true});
                return get('agent_external_read', {id: contributorId, diff: true}).then(res => {
                    Agent.update({where: contributorId, data: res});
                    Agent.updateMeta(contributorId, {is_dirty: true});
                }).finally(() => Agent.updateMeta(contributorId, {syncing: false}));
            },
            toggleActivity(context, activityId) {
                let activity = Activity.query().with('meta').find(activityId);
                Activity.updateMeta(activityId, {'to_delete': !activity.meta.to_delete});
            },
            purgeTemporary(context) {
                Meta.query().where('is_temporary', true).with('item').get().forEach(m => {
                    m.item.$delete();
                });
            }
        }
    }
);

export default store;