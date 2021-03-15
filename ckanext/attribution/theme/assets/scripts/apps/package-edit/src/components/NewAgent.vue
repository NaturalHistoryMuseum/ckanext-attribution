<template>
    <div class="agent-edit-block agent-detail" :class="'agent-'+editedDetails.agent_type.toLowerCase()">
        <div class="agent-header">
            <template v-if="manual || needsImport">
                <div class="agent-type-edit">
                    <span v-for="(iconName, agentType) in iconDict" class="agent-type-option">
                        <input type="radio" :value="agentType" v-model="editedDetails.agent_type"
                               :id="'agent-type-option-' + agentType + '-new'">
                        <label :for="'agent-type-option-' + agentType + '-new'">
                            <i class="fas" :class="'fa-' + iconName"></i>
                        </label>
                    </span>
                </div>
                <span class="display-name">
                    <em>{{ displayName }}</em>
                </span>
            </template>
            <div class="agent-name" v-if="!manual && !needsImport">
                <i class="fas agent-icon" :class="typeIcon(details.agent_type)"></i>
                <b>{{ details.standardised_name }}</b>
            </div>
            <div class="agent-identifier" v-if="(!manual) && details.external_id">
                <a :href="details.external_id_url" v-if="details.external_id">
                    <i :class="identifierIcon(details.external_id_scheme)"></i> {{ details.external_id }}
                </a>
                <a :href="'/user/' + details.user_id" v-if="details.user_id" target="_blank">
                    <i class="far fa-smile"></i> user profile
                </a>
            </div>
        </div>
        <div class="agent-name-edit attribution-row" v-if="manual">
            <template v-if="editedDetails.agent_type === 'individual'">
                <text-field v-model="editedDetails.family_name" :cls="['wrap-small']">
                    Family name
                </text-field>
                <text-field v-model="editedDetails.given_names" :cls="['wrap-small']">
                    Given name(s)
                </text-field>
                <div class="attribution-field one-line" v-for="fieldId in idGen">
                    <label :for="fieldId">
                        Given names first
                    </label>
                    <input :id="fieldId" type="checkbox" v-model="editedDetails.given_names_first">
                </div>
                <help-tooltip>
                    Does this person's culture typically place given or family names first? (this
                    does not affect sorting)
                </help-tooltip>
            </template>
            <template v-if="editedDetails.agent_type !== 'individual'">
                <text-field v-model="editedDetails.name" :oneline="true">
                    Name
                </text-field>
            </template>
        </div>
        <div class="agent-user-edit attribution-row" v-if="manual || needsImport">
            <autocomplete-field v-model="editedDetails.user_id" @typing="updateUserOptions" :options="userOptions"
                                label="Associated user" item-id="agent-user-new">
            </autocomplete-field>
            <help-tooltip>
                If this contributor has a user account registered on the portal, associate it here
            </help-tooltip>
        </div>
        <EditActivity :details="{}" :agent="editedDetails"></EditActivity>
        <div class="agent-save">
            <span class="btn btn-primary" @click="saveChanges">
                <i class="fas fa-plus"></i>
                {{ needsImport ? 'Import' : manual ? 'Create' : 'Add' }}
            </span>
            <span class="btn btn-primary" @click="$emit('toggle-edit')">
                <i class="fas fa-times"></i>
                Cancel
            </span>
        </div>
    </div>
</template>

<script>
import {mapGetters} from 'vuex';
import {post} from '../api';
import EditAgent from './EditAgent.vue';
import EditActivity from './EditActivity.vue';
import {eventBus, events} from '../eventbus';

export default {
    name: 'NewAgent',
    components: {EditActivity},
    extends: EditAgent,
    data: function () {
        return {}
    },
    computed: {
        ...mapGetters(['typeIcon']),
        needsImport() {
            return (!this.details.id) && this.details.external_id;
        },
        manual() {
            return (!this.details.id) && (!this.details.external_id)
        }
    },
    methods: {
        saveChanges() {
            if (this.needsImport || this.manual) {
                post('agent_create', this.editedDetails).then(d => {
                    this.$set(this.editedDetails, 'id', d.result.id);
                    eventBus.$emit(events.saveActivity);
                    eventBus.$on(events.closeActivity, () => {
                        this.$emit('toggle-edit');
                    })
                }).catch((e) => {
                    console.error(e)
                });
            }

            if (!this.needsImport) {
                eventBus.$emit(events.saveActivity, () => {
                    console.log('success');
                });
                this.$emit('toggle-edit');
            }
        },
    },
    created: function () {
        this.resetEdits();
    },
    watch: {
        details() {
            this.editedDetails = {};
            this.resetEdits();
        }
    }
}
</script>