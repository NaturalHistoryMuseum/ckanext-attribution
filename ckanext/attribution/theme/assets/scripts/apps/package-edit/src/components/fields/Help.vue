<template>
    <div class="help-icon">
        <i class="fas fa-question-circle"></i>
        <div class="help-tooltip" role="tooltip">
            <slot></slot>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Help',
}
</script>