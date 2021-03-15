<template>
    <div>
        <label>Contributors</label>
        <ContributionBlock v-for="agent in agents" :key="agent.agent.id" :agent="agent.agent"
                           :activities="agent.activities"/>
        <AgentSearch></AgentSearch>
    </div>
</template>

<script>
import ContributionBlock from './components/ContributionBlock.vue';
import {mapActions, mapGetters, mapMutations, mapState} from 'vuex';
import AgentSearch from './components/AgentSearch.vue';
import EditActivity from './components/EditActivity.vue';

export default {
    name: 'App',
    components: {
        EditActivity,
        AgentSearch,
        ContributionBlock,
    },
    data: function () {
        return {
        }
    },
    props: ['packageId', 'canEdit'],
    computed: {
        ...mapState(['contributions']),
        ...mapGetters(['agents'])
    },
    methods: {
        ...mapActions(['getContributions', 'getSchemes']),
        ...mapMutations(['setPackageId', 'setEditPermission'])
    },
    created: function () {
        this.setPackageId(this.packageId);
        // TODO
        this.setEditPermission(this.canEdit === 'True');
        this.getContributions();
        this.getSchemes();
    }
}
</script>