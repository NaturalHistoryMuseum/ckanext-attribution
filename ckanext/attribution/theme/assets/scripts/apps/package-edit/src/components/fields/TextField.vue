<template>
    <div :class="classes">
        <label :for="fieldId">
            <slot></slot>
        </label>
        <input type="text" :value="value" :id="fieldId" :placeholder="placeholder" @change="setValue">
    </div>
</template>

<script>
import Field from './Field.vue';

export default {
    name: 'TextField',
    extends: Field,
    props: ['placeholder']
}
</script>
