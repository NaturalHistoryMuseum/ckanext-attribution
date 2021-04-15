<template>
    <div :class="blockClasses">
        <div class="agent-header">
            <div class="agent-name">
                <i class="fas agent-icon" :class="agentTypeIcon(contributor.agent_type)"></i>
                <b>{{ contributor.standardisedName }}</b>
            </div>
            <div class="edit-icons">
                <span class="edit-icon" title="Download contributor details from external source"
                      v-if="contributor.external_id" @click="syncAgent(contributorId)">
                    <i class="fas" :class="contributor.meta.syncing ? 'fa-spinner fa-spin' : 'fa-arrow-alt-circle-down'"></i>
                </span>
                <span class="edit-icon" title="Edit" v-if="canEdit" @click="$emit('toggle-edit')">
                    <i class="fas fa-edit"></i>
                </span>
                <span class="edit-icon" title="Remove this contributor"
                      @click="eventBus.$emit(events.removeContributor, contributorId)">
                    <i class="fas fa-minus-circle"></i>
                </span>
            </div>
        </div>
        <div class="agent-identifier">
            <a :href="contributor.externalIdUrl" v-if="contributor.external_id">
                <i :class="agentIdIcon(contributor.external_id_scheme)"></i> {{ contributor.external_id }}
            </a>
            <a :href="'/user/' + contributor.user_id" v-if="contributor.user_id" target="_blank">
                <i class="far fa-smile"></i> user profile
            </a>
        </div>
        <div class="agent-affiliations">
            <span class="agent-affiliation" v-for="affiliation in affiliations.slice(0, affiliationLimit)">
                {{ affiliation.other_agent.displayName }} <template v-if="affiliation.affiliation_type">({{
                    affiliation.affiliation_type
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
import Common from './Common.vue';
import Agent from '../models/agent';

export default {
    name    : 'ShowAgent',
    extends : Common,
    data    : function () {
        return {
            affiliationLimit: 5
        }
    },
    computed: {
        ...mapState(['canEdit', 'controlledLists']),
        ...mapGetters(['agentIdIcon', 'agentTypeIcon']),
        affiliations() {
            return Agent.query()
                        .with('affiliations.other_agent')
                        .with('affiliations.meta')
                        .find(this.contributorId).affiliations.filter(a => !a.meta.to_delete);
        },
        blockClasses() {
            let classes = ['agent-detail', `agent-${this.contributor.agent_type.toLowerCase()}`]
            if (this.contributor.meta.is_dirty) {
                classes.push('agent-dirty');
            }
            if (this.contributor.activities.filter(a => !a.meta.to_delete).length === 0) {
                classes.push('agent-empty');
            }
            return classes;
        }
    },
    methods : {
        ...mapActions(['syncAgent'])
    }
}
</script>