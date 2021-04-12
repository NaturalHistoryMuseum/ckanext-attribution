import {Model} from '@vuex-orm/core';

export default class Meta extends Model {

    static entity = 'metadata';

    static fields() {
        return {
            id        : this.uid(),
            item_id   : this.attr(null),
            item_type : this.attr(null),
            is_hidden : this.boolean(false),
            is_editing: this.boolean(false),
            to_delete : this.boolean(false),
            is_dirty  : this.boolean(false),
            syncing   : this.boolean(false),
            is_new    : this.boolean(false)
        }
    }
}