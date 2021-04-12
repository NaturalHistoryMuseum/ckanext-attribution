<template>

</template>

<script>
import {mapState} from 'vuex';
import {eventBus, events} from '../eventbus';
import Agent from '../models/agent';

export default {
    name    : 'Common',
    props   : ['contributorId'],
    data    : function () {
        return {
            eventBus   : eventBus,
            events     : events
        }
    },
    computed: {
        contributor() {
            return Agent.query().with('meta').with('citation').find(this.contributorId);
        }
    }
}
</script>