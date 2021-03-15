import Vue from 'vue';
import Vuex from 'vuex';
import {get, post} from '../api';

Vue.use(Vuex);

const store = new Vuex.Store(
    {
        state: {
            packageId: null,
            canEdit: false,
            contributions: [],
            iconDict: {
                individual: 'user',
                org: 'building',
                other: 'asterisk'
            },
            schemeDict: [],
            roleList: [],
            levelList: [
                'Lead',
                'Equal',
                'Supporting'
            ]
        },
        getters: {
            agents: state => {
                let agent_list = {};
                state.contributions.forEach((c) => {
                    if (agent_list[c.agent.id]) {
                        agent_list[c.agent.id].activities.push(c.contribution_activity)
                    } else {
                        agent_list[c.agent.id] = {
                            agent: c.agent,
                            activities: [c.contribution_activity]
                        }
                    }
                })
                return agent_list
            },
            activities: state => {
                let activity_list = {}
                state.contributions.forEach(c => {
                    let name = c.contribution_activity.activity;
                    if (activity_list[name]) {
                        activity_list[name].push(c.contribution_activity)
                    } else {
                        activity_list[name] = [c.contribution_activity]
                    }
                })
                return activity_list;
            },
            similarActivity: state => (activityName) => {
                if (!activityName) {
                    return [];
                }
                return state.contributions.filter((c) => {
                    return c.contribution_activity.activity.toLowerCase() === activityName.toLowerCase();
                });
            },
            typeIcon: state => (agentType) => {
                return 'fas fa-' + state.iconDict[agentType.toLowerCase()];
            },
            identifierIcon: state => (schemeName) => {
                if (schemeName === 'orcid') {
                    return 'fab fa-orcid';
                } else if (schemeName === 'ror') {
                    return 'fas fa-university'
                } else {
                    return 'fas fa-link';
                }
            },
            identifierType: state => (schemeName) => {
                if (!schemeName) {
                    return null;
                }
                return state.schemeDict.filter(s => s.name === schemeName.toLowerCase())[0];
            },
            defaultIdentifierType: state => (agentType) => {
                return state.schemeDict.filter(s => s.details.default.includes(agentType))[0];
            }
        },
        mutations: {
            setPackageId(state, payload) {
                Vue.set(state, 'packageId', payload)
            },
            setEditPermission(state, payload) {
                Vue.set(state, 'canEdit', payload)
            },
            addContributors(state, payload) {
                state.contributions = [...payload];
            }
        },
        actions: {
            getContributions(context) {
                let url = 'package_contributions_show?id=' + context.state.packageId;
                get(url).then(d => {
                    context.commit('addContributors', d.result);
                })
            },
            getRoles(context) {
                return get('contribution_roles_list').then(d => {
                    if (d.success) {
                        context.state.roleList = Object.entries(d.result).map(r => {
                            return {'label': r[0], 'credit': r[1]}
                        });
                    }
                }).catch(e => console.error(e));
            },
            getSchemes(context) {
                get('external_id_schemes').then(d => {
                    if (d.success) {
                        context.state.schemeDict = Object.entries(d.result).map(r => {
                            return {'name': r[0], 'details': r[1]}
                        });
                    }
                }).catch(e => console.error(e));
            },
            updateAgent(context, agentId) {
                let url = 'agent_show?id=' + agentId;
                get(url).then(d => {
                    if (!d.success) {
                        console.error('Unable to update.')
                        return;
                    }
                    context.state.contributions = context.state.contributions.map(c => {
                        if (c.agent.id === agentId) {
                            c.agent = d.result;
                        }
                        return c;
                    })
                })
            },
            updateActivities(context, activityName) {
                context.state.contributions.forEach((c, i) => {
                    if (c.contribution_activity.activity !== activityName) {
                        return;
                    }
                    let url = 'contribution_activity_show?id=' + c.contribution_activity.id;
                    get(url).then(d => {
                        if (!d.success) {
                            console.error('Unable to update.')
                            return;
                        }
                        Vue.set(context.state.contributions[i], 'contribution_activity', d.result);
                    })
                })
            },
            externalUpdate(context, agentId) {
                return post('agent_external_update', {id: agentId}).then(d => {
                    if (!d.success) {
                        console.error('Unable to update.')
                        return;
                    }
                    context.state.contributions = context.state.contributions.map(c => {
                        if (c.agent.id === agentId) {
                            c.agent = d.result;
                        }
                        return c;
                    })
                });
            },
            removeAgent(context, agentId) {
                let contribution = context.getters.agents[agentId];
                contribution.activities.forEach(a => context.dispatch('removeActivity', a.id))
            },
            removeActivity(context, activityId) {
                let activity = context.state.contributions.filter(c => {
                    return c.contribution_activity.id === activityId
                })[0].contribution_activity;
                if (activity.order) {
                    context.getters.activities[activity.activity].filter(a => {
                        return a.id !== activityId && a.order && a.order >= activity.order;
                    }).sort((a, b) => a.order - b.order).forEach((a, i) => {
                        post('contribution_activity_update', {
                            id: a.id,
                            order: activity.order + i
                        }).then(d => {
                            let i = context.state.contributions.map(c => c.contribution_activity.id).indexOf(d.result.id);
                            Vue.set(context.state.contributions[i].contribution_activity, 'order', d.result.order);
                        }).catch(e => console.error(e))
                    })
                }

                return post('contribution_activity_delete', {id: activityId}).then(d => {
                    if (!d.success) {
                        console.error(d);
                        return;
                    }
                    context.state.contributions = context.state.contributions.filter(c => {
                        return c.contribution_activity.id !== activityId;
                    })
                })
            }
        }
    }
);

export default store;