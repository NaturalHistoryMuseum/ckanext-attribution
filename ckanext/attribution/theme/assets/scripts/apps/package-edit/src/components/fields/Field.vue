<template>
    <div :class="classes">
        <label :for="fieldId">
            <slot></slot>
        </label>
        <input :type="inputType" :value="value" :id="fieldId" @change="setValue">
    </div>
</template>

<script>
import {nanoid} from 'nanoid';

export default {
    name: 'Field',
    props: ['value', 'inputType', 'cls'],
    data: function () {
        return {
            fieldId: nanoid(8)
        }
    },
    computed: {
        classes() {
            let classList = ['attribution-field'];
            if (this.cls) {
                classList = classList.concat(this.cls);
            }
            return classList;
        }
    },
    methods: {
        setValue(event) {
            this.$emit('input', event.target.value);
        }
    }
}
</script>

<style scoped>

</style>