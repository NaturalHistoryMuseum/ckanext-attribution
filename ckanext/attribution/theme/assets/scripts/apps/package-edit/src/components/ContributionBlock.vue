<template>
    <div class="contribution-block">
        <Agent :details="agent" v-if="!agentEditing" v-on:toggle-edit="toggleAgentEdit" :affiliations="affiliations"/>
        <EditAgent :details="agent" v-if="agentEditing" v-on:toggle-edit="toggleAgentEdit"
                   :affiliations="affiliations"/>
        <div class="agent-activities">
            <Activity v-for="activity in activities" :key="activity.id" :details="activity" :editing="activityEditing && activityEditing.id === activity.id"
                      v-on:toggle-edit="toggleActivityEdit(activity)"/>
            <span @click="$emit('save-activity')" v-if="activityCreating" class="icon-btn">
                <i class="fas fa-lg fa-check-circle"></i>
            </span>
            <span @click="toggleActivityEdit({})" class="icon-btn">
                <i class="fas fa-lg" :class="activityCreating ? 'fa-times-circle' : 'fa-plus-circle'"></i>
            </span>
        </div>
        <EditActivity v-if="activityEditing" :details="activityEditing" :other-roles="otherRoles" :agent="agent"
                      v-on:save-edit="saveActivityEdit" v-on:toggle-edit="toggleActivityEdit(activityEditing)"/>
    </div>
</template>

<script>
import Agent from './Agent.vue';
import Activity from './Activity.vue';
import EditAgent from './EditAgent.vue';
import EditActivity from './EditActivity.vue';
import {get} from '../api';
import {mapActions, mapState} from 'vuex';

export default {
    name: 'ContributionBlock',
    props: ['agent', 'activities'],
    components: {
        EditAgent,
        EditActivity,
        Activity,
        Agent
    },
    data: function () {
        return {
            agentEditing: false,
            activityEditing: null,
            affiliations: []
        }
    },
    computed: {
        ...mapState(['packageId', 'roleList']),
        otherRoles() {
            return this.activities.map(a => a.activity).filter(a => (a !== this.activityEditing.activity) || !this.activityEditing.activity)
        },
        activityCreating() {
            return this.activityEditing && !this.activityEditing.id;
        }
    },
    methods: {
        ...mapActions(['updateAgent']),
        toggleAgentEdit() {
            if (this.agentEditing) {
                this.updateAgent(this.agent.id);
                this.getAffiliations();
            }
            this.agentEditing = !this.agentEditing;
        },
        getAffiliations() {
            let url = 'agent_all_affiliations?agent_id=' + this.agent.id;
            get(url).then(d => {
                this.affiliations = d.result.filter(x => {
                    return (x.affiliation.package_id === this.packageId) || (x.affiliation.package_id === null);
                });
            })
        },
        toggleActivityEdit(activity) {
            if (this.activityEditing === null || this.activityEditing.id !== activity.id) {
                this.activityEditing = activity;
            } else {
                this.activityEditing = null;
            }
        },
        saveActivityEdit() {
            this.activityEditing = null;
        }
    },
    created() {
        this.getAffiliations();
    }
}
</script>