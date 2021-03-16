<template>
    <div class="activity-edit-block">
        <div class="activity-edit-fields attribution-row">
            <select-field v-model="editedDetails.activity" :options="filteredRoles" :opt-value="o => o.credit"
                          :opt-label="o => o.label" @input="getAgents">
                Contribution role
            </select-field>
            <select-field v-model="editedDetails.level" :options="levelList">
                Contribution level
            </select-field>
            <div class="attribution">
                <label>Contribution date</label>
                <DatePicker v-model="editedDetails.time" type="datetime" placeholder="Select date/time (optional)"
                            :show-time-panel="timePicker">
                    <template v-slot:footer>
                        <button class="mx-btn mx-btn-text" @click="timePicker = !timePicker">
                            {{ timePicker ? 'select date' : 'select time' }}
                        </button>
                    </template>
                </DatePicker>
            </div>
        </div>
        <div class="activity-sorted-agents attribution-row">
            <div><b>Ordered contributors</b></div>
            <div class="help-icon">
                <i class="fas fa-question-circle"></i>
                <div class="help-tooltip" role="tooltip">
                    Contributors that should be listed in a particular order when citing.
                </div>
            </div>
            <draggable v-model="sortedAgents" group="allAgents" @change="updateOrder">
                <div v-for="item in sortedAgents" class="activity-agent"
                     :class="item.id === details.id ? 'active-agent' : ''">
                    <i class="fas fa-arrows"></i>
                    <span>{{ item.name }}</span>
                    <span>{{ item.order }}</span>
                </div>
            </draggable>
        </div>
        <div class="activity-unsorted-agents attribution-row">
            <div><b>Unordered contributors</b></div>
            <div class="help-icon">
                <i class="fas fa-question-circle"></i>
                <div class="help-tooltip" role="tooltip">
                    Contributors that do not have to be listed in any particular order. These will be listed
                    <em>after</em> the ordered contributors.
                </div>
            </div>
            <draggable v-model="unsortedAgents" group="allAgents" @change="updateOrder">
                <div v-for="item in unsortedAgents" class="activity-agent"
                     :class="item.id === details.id ? 'active-agent' : ''">
                    <i class="fas fa-arrows"></i>
                    <span>{{ item.name }}</span>
                    <span>{{ item.order }}</span>
                </div>
            </draggable>
        </div>
        <div class="activity-save" v-if="editedDetails.id !== 'new'">
            <span class="btn btn-primary" @click="saveChanges">
                <i class="fas fa-save"></i>
                Save changes
            </span>
            <span class="btn btn-primary" @click="$emit('toggle-edit')">
                <i class="fas fa-times"></i>
                Cancel
            </span>
        </div>
    </div>
</template>

<script>
import {mapActions, mapGetters, mapState} from 'vuex';
import cloneDeep from 'lodash.clonedeep';
import draggable from 'vuedraggable';
import DatePicker from 'vue2-datepicker';
import 'vue2-datepicker/index.css';
import {post} from '../api';
import {eventBus, events} from '../eventbus';

export default {
    name: 'EditActivity',
    components: {
        draggable,
        DatePicker
    },
    props: {
        details: {
            default: () => {
                return {}
            }
        },
        otherRoles: {default: () => []},
        agent: Object
    },
    data: function () {
        return {
            editedDetails: {},
            sortedAgents: [],
            unsortedAgents: [],
            timePicker: false,
            waitingToSave: false
        }
    },
    computed: {
        ...mapState(['roleList', 'levelList', 'packageId']),
        ...mapGetters(['similarActivity']),
        filteredRoles() {
            return this.roleList.filter(r => !this.otherRoles.includes(r.credit));
        },
        agentDisplayName() {
            if (this.agent.display_name) {
                return this.agent.display_name;
            }
            if ((!this.agent.name) && (!this.agent.family_name) && (!this.agent.given_names)) {
                return 'New Contributor';
            }
            if (this.agent.agent_type === 'individual') {
                let nameParts = [this.agent.given_names, this.agent.family_name];
                return this.agent.given_names_first ? nameParts.join(' ') : nameParts.reverse().join(' ')
            } else {
                return this.agent.name;
            }
        }
    },
    methods: {
        ...mapActions(['getRoles', 'updateActivities', 'getContributions']),
        getAgents(input) {
            this.$set(this.editedDetails, 'activity', input);
            let allAgents = this.similarActivity(this.editedDetails.activity).map(a => {
                return {
                    name: a.agent.display_name,
                    id: a.contribution_activity.id,
                    order: a.contribution_activity.order
                }
            });
            this.sortedAgents = allAgents.filter(a => a.order !== null);
            this.unsortedAgents = allAgents.filter(a => a.order === null);
            if (!this.details.id) {
                this.unsortedAgents.push({
                    name: this.agentDisplayName,
                    id: null,
                    order: null
                })
            }
        },
        updateOrder() {
            this.sortedAgents = this.sortedAgents.map((a, i) => {
                a.order = i + 1;
                if (a.id === this.details.id) {
                    this.$set(this.editedDetails, 'order', i + 1)
                }
                return a;
            });
            this.unsortedAgents = this.unsortedAgents.map((a) => {
                a.order = null;
                if (a.id === this.details.id) {
                    this.$set(this.editedDetails, 'order', null)
                }
                return a;
            })
        },
        saveChanges() {
            console.log('saving');
            // double check the id
            this.editedDetails.id = this.details.id;
            let promises = []
            if (this.details.id) {
                promises.push(post('contribution_activity_update', this.editedDetails).catch((e) => {
                    console.error(e)
                }));
            } else {
                let body = {...this.editedDetails}
                body.agent_id = this.agent.id;
                body.package_id = this.packageId;
                body.order = this.sortedAgents.concat(this.unsortedAgents).filter(a => !a.id)[0].order;
                promises.push(post('contribution_activity_create', body).then(d => {
                    this.$set(this.editedDetails, 'id', d.result.id);
                }).catch((e) => {
                    console.error(e)
                }));
            }

            this.sortedAgents.concat(this.unsortedAgents).forEach(a => {
                if (!a.id) {
                    return
                }
                promises.push(post('contribution_activity_update', {id: a.id, order: a.order}));
            })

            if (this.details.id) {
                this.updateActivities(this.editedDetails.activity);
            } else {
                this.getContributions();
            }

            return Promise.all(promises).then(() => {
                    eventBus.$emit(events.closeActivity, this.editedDetails.id)
                }
            ).catch(e => console.error(e)).finally(() => {
                this.waitingToSave = false;
            });
        },
        refresh() {
            this.editedDetails = cloneDeep(this.details);
            if (!this.details.id) {
                this.$set(this.editedDetails, 'id', 'new')
            }
            this.getAgents(this.editedDetails.activity || this.filteredRoles[0].credit);
        }
    },
    created: function () {
        this.getRoles().then(() => this.refresh());
        eventBus.$on(events.saveActivity, () => {
            if (this.details.id || this.agent.id) {
                this.saveChanges()
            }
            else {
                this.waitingToSave = true;
            }
        })
    },
    watch: {
        details() {
            this.refresh();
        },
        agent: {
            handler(v, o) {
                if (v.id && v.id !== o.id && this.waitingToSave) {
                    this.saveChanges();
                }
            },
            deep: true
        }
    }
}
</script>