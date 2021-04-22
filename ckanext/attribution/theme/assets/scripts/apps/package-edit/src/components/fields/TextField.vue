<template>
    <div :class="classes">
        <label :for="fieldId">
            <slot></slot>
        </label>
        <input class="form-control" type="text" :value="value" :id="fieldId" :placeholder="placeholder" @input="debouncedSetValue">
    </div>
</template>

<script>
import Field from './Field.vue';
import debounce from 'lodash.debounce';

export default {
    name: 'TextField',
    extends: Field,
    props: ['placeholder'],
    created() {
        this.debouncedSetValue = debounce(this.setValue, 200);
    },
}
</script>
