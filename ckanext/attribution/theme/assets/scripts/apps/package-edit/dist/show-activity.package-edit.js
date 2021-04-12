(window["webpackJsonppackage_edit"] = window["webpackJsonppackage_edit"] || []).push([[3],{

/***/ 76:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// CONCATENATED MODULE: ./node_modules/vue-loader/lib/loaders/templateLoader.js??vue-loader-options!./node_modules/vue-loader/lib??vue-loader-options!./src/components/ShowActivity.vue?vue&type=template&id=664d035c&
var render = function() {
  var _vm = this
  var _h = _vm.$createElement
  var _c = _vm._self._c || _h
  return _c(
    "div",
    {
      staticClass: "agent-activity",
      class: [
        { "is-deleted": _vm.activity.meta.to_delete },
        "activity-scheme-" + _vm.activity.scheme
      ]
    },
    [
      _c(
        "div",
        {
          staticClass: "clickable-text",
          class: { clicked: _vm.activity.meta.is_editing },
          on: { click: _vm.toggleEdit }
        },
        [
          _c("span", [_vm._v(_vm._s(_vm.activity.activity))]),
          _vm._v(" "),
          _vm.activity.order
            ? _c("span", [_vm._v(" (#" + _vm._s(_vm.activity.order) + ")")])
            : _vm._e()
        ]
      ),
      _vm._v(" "),
      _c("i", {
        staticClass: "fas fa-sm fa-minus-circle",
        on: {
          click: function($event) {
            return _vm.toggleActivity(_vm.activityId)
          }
        }
      })
    ]
  )
}
var staticRenderFns = []
render._withStripped = true


// CONCATENATED MODULE: ./src/components/ShowActivity.vue?vue&type=template&id=664d035c&

// EXTERNAL MODULE: ./node_modules/vuex/dist/vuex.esm.js
var vuex_esm = __webpack_require__(3);

// EXTERNAL MODULE: ./src/models/activity.js
var models_activity = __webpack_require__(12);

// CONCATENATED MODULE: ./node_modules/babel-loader/lib!./node_modules/vue-loader/lib??vue-loader-options!./src/components/ShowActivity.vue?vue&type=script&lang=js&
function ownKeys(a,b){var c=Object.keys(a);if(Object.getOwnPropertySymbols){var d=Object.getOwnPropertySymbols(a);b&&(d=d.filter(function(b){return Object.getOwnPropertyDescriptor(a,b).enumerable})),c.push.apply(c,d)}return c}function _objectSpread(a){for(var b,c=1;c<arguments.length;c++)b=null==arguments[c]?{}:arguments[c],c%2?ownKeys(Object(b),!0).forEach(function(c){_defineProperty(a,c,b[c])}):Object.getOwnPropertyDescriptors?Object.defineProperties(a,Object.getOwnPropertyDescriptors(b)):ownKeys(Object(b)).forEach(function(c){Object.defineProperty(a,c,Object.getOwnPropertyDescriptor(b,c))});return a}function _defineProperty(a,b,c){return b in a?Object.defineProperty(a,b,{value:c,enumerable:!0,configurable:!0,writable:!0}):a[b]=c,a}//
//
//
//
//
//
//
//
//
//
/* harmony default export */ var ShowActivityvue_type_script_lang_js_ = ({name:"ShowActivity",props:["activityId"],data:function data(){return{}},computed:{activity:function activity(){return models_activity["a" /* default */].query()["with"]("meta").find(this.activityId)}},methods:_objectSpread(_objectSpread({},Object(vuex_esm["b" /* mapActions */])(["toggleActivity"])),{},{toggleEdit:function toggleEdit(){this.activity.meta.to_delete&&this.toggleActivity(this.activityId),this.$emit("toggle-edit")}})});
// CONCATENATED MODULE: ./src/components/ShowActivity.vue?vue&type=script&lang=js&
 /* harmony default export */ var components_ShowActivityvue_type_script_lang_js_ = (ShowActivityvue_type_script_lang_js_); 
// EXTERNAL MODULE: ./node_modules/vue-loader/lib/runtime/componentNormalizer.js
var componentNormalizer = __webpack_require__(1);

// CONCATENATED MODULE: ./src/components/ShowActivity.vue





/* normalize component */

var component = Object(componentNormalizer["a" /* default */])(
  components_ShowActivityvue_type_script_lang_js_,
  render,
  staticRenderFns,
  false,
  null,
  null,
  null
  
)

/* hot reload */
if (false) { var api; }
component.options.__file = "src/components/ShowActivity.vue"
/* harmony default export */ var ShowActivity = __webpack_exports__["default"] = (component.exports);

/***/ })

}]);