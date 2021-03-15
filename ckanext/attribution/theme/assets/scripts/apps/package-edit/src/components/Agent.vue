<template>
    <div class="agent-detail" :class="'agent-'+details.agent_type.toLowerCase()">
        <div class="agent-header">
            <div class="agent-name">
                <i class="fas agent-icon" :class="typeIcon(details.agent_type)"></i>
                <b>{{ details.standardised_name }}</b>
            </div>
            <div class="edit-icons">
                <span class="edit-icon" title="Download details from external source"
                      v-if="details.external_id" @click="updateFromExternal">
                    <i class="fas" :class="syncing ? 'fa-spinner fa-spin' : 'fa-arrow-alt-circle-down'"></i>
                </span>
                <span class="edit-icon" v-if="canEdit" title="Edit" @click="$emit('toggle-edit')">
                    <i class="fas fa-edit"></i>
                </span>
                <span class="edit-icon" title="Remove this contributor" @click="removeAgent(details.id)">
                    <i class="fas fa-minus-circle"></i>
                </span>
            </div>
        </div>
        <div class="agent-identifier">
            <a :href="details.external_id_url" v-if="details.external_id">
                <i :class="identifierIcon(details.external_id_scheme)"></i> {{ details.external_id }}
            </a>
            <a :href="'/user/' + details.user_id" v-if="details.user_id" target="_blank">
                <i class="far fa-smile"></i> user profile
            </a>
        </div>
        <div class="agent-affiliations">
            <span class="agent-affiliation" v-for="affiliation in affiliations.slice(0, affiliationLimit)">
                {{ affiliation.agent.display_name }} <template v-if="affiliation.affiliation.affiliation_type">({{
                    affiliation.affiliation.affiliation_type
                }})</template>
            </span>
            <span v-if="affiliations.length > affiliationLimit" class="agent-affiliation">
                {{ affiliations.length - affiliationLimit }} more
            </span>
        </div>
    </div>
</template>

<script>
import {mapActions, mapGetters, mapState} from 'vuex';

export default {
    name: 'Agent',
    props: ['details', 'affiliations'],
    data: function () {
        return {
            affiliationLimit: 5,
            syncing: false
        }
    },
    computed: {
        ...mapState(['canEdit', 'iconDict']),
        ...mapGetters(['identifierIcon', 'typeIcon'])
    },
    methods: {
        ...mapActions(['externalUpdate', 'removeAgent']),
        updateFromExternal() {
            this.syncing = true;
            this.externalUpdate(this.details.id).finally(() => {
                this.syncing = false;
            });
        }
    }
}
</script>