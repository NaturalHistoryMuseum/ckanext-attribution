import Vue from 'vue';

const events = {
    saveActivity: 'save-activity',
    closeActivity: 'close-activity'
}

const eventBus = new Vue();

export {eventBus, events};