<template>
    <div class="agent-activity">
        <span class="clickable-text" :class="{'clicked': editing}" @click="$emit('toggle-edit')">{{ details.activity }}</span>
        <span v-if="details.order"> (#{{ details.order }})</span>
        <i class="fas fa-sm fa-minus-circle" @click="removeActivity(details.id)"></i>
    </div>
</template>

<script>
import {mapActions} from 'vuex';

export default {
    name: 'Activity',
    props: ['details', 'editing'],
    data: function () {
        return {
        }
    },
    methods: {
        ...mapActions(['removeActivity'])
    }
}
</script>