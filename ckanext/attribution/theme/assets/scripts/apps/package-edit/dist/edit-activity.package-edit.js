(window["webpackJsonppackage_edit"] = window["webpackJsonppackage_edit"] || []).push([[0],{

/***/ 74:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// CONCATENATED MODULE: ./node_modules/vue-loader/lib/loaders/templateLoader.js??vue-loader-options!./node_modules/vue-loader/lib??vue-loader-options!./src/components/EditActivity.vue?vue&type=template&id=dbad2a2e&
var render = function() {
  var _vm = this
  var _h = _vm.$createElement
  var _c = _vm._self._c || _h
  return _c(
    "div",
    { staticClass: "activity-edit-block" },
    [
      _c(
        "div",
        { staticClass: "activity-edit-fields attribution-row" },
        [
          _c(
            "select-field",
            {
              attrs: {
                options: Object.keys(_vm.controlledLists.activityTypes)
              },
              on: {
                input: function($event) {
                  return _vm.getOptions(_vm.edits.scheme)
                }
              },
              model: {
                value: _vm.edits.scheme,
                callback: function($$v) {
                  _vm.$set(_vm.edits, "scheme", $$v)
                },
                expression: "edits.scheme"
              }
            },
            [_vm._v("\n            Role scheme\n        ")]
          ),
          _vm._v(" "),
          _vm.edits.scheme
            ? _c(
                "select-field",
                {
                  attrs: {
                    options: _vm.activityOptions,
                    "opt-value": function(o) {
                      return o.name
                    },
                    "opt-label": function(o) {
                      return o.name
                    }
                  },
                  on: { input: _vm.getAgents },
                  model: {
                    value: _vm.edits.activity,
                    callback: function($$v) {
                      _vm.$set(_vm.edits, "activity", $$v)
                    },
                    expression: "edits.activity"
                  }
                },
                [_vm._v("\n            Contribution role\n        ")]
              )
            : _vm._e(),
          _vm._v(" "),
          _c(
            "select-field",
            {
              attrs: { options: _vm.controlledLists.activityLevels },
              model: {
                value: _vm.edits.level,
                callback: function($$v) {
                  _vm.$set(_vm.edits, "level", $$v)
                },
                expression: "edits.level"
              }
            },
            [_vm._v("\n            Contribution level\n        ")]
          ),
          _vm._v(" "),
          _c(
            "div",
            { staticClass: "attribution" },
            [
              _c(
                "datefield",
                {
                  attrs: { placeholder: "Select date (optional)" },
                  model: {
                    value: _vm.edits.time,
                    callback: function($$v) {
                      _vm.$set(_vm.edits, "time", $$v)
                    },
                    expression: "edits.time"
                  }
                },
                [_vm._v("\n                Contribution date\n            ")]
              )
            ],
            1
          )
        ],
        1
      ),
      _vm._v(" "),
      _c(
        "div",
        {
          staticClass: "expand-bar",
          attrs: { title: "Expand" },
          on: {
            click: function($event) {
              _vm.expand = !_vm.expand
            }
          }
        },
        [
          _c("i", {
            staticClass: "fas",
            class: _vm.expand ? "fa-caret-up" : "fa-caret-down"
          }),
          _vm._v(" "),
          _c("small", [_vm._v("Advanced options")]),
          _vm._v(" "),
          _c("i", {
            staticClass: "fas",
            class: _vm.expand ? "fa-caret-up" : "fa-caret-down"
          })
        ]
      ),
      _vm._v(" "),
      _vm.expand
        ? [
            _c(
              "div",
              { staticClass: "activity-sorted-agents attribution-row" },
              [
                _vm._m(0),
                _vm._v(" "),
                _vm._m(1),
                _vm._v(" "),
                _c(
                  "draggable",
                  {
                    attrs: { group: "allAgents" },
                    on: { change: _vm.updateOrder },
                    model: {
                      value: _vm.sortedAgents,
                      callback: function($$v) {
                        _vm.sortedAgents = $$v
                      },
                      expression: "sortedAgents"
                    }
                  },
                  _vm._l(_vm.sortedAgents, function(item) {
                    return _c(
                      "div",
                      {
                        staticClass: "activity-agent",
                        class: item.id === _vm.activityId ? "active-agent" : ""
                      },
                      [
                        _c("i", { staticClass: "fas fa-arrows" }),
                        _vm._v(" "),
                        _c("span", [_vm._v(_vm._s(item.name))]),
                        _vm._v(" "),
                        _c("span", [_vm._v(_vm._s(item.order))])
                      ]
                    )
                  }),
                  0
                )
              ],
              1
            ),
            _vm._v(" "),
            _c(
              "div",
              { staticClass: "activity-unsorted-agents attribution-row" },
              [
                _vm._m(2),
                _vm._v(" "),
                _vm._m(3),
                _vm._v(" "),
                _c(
                  "draggable",
                  {
                    attrs: { group: "allAgents" },
                    on: { change: _vm.updateOrder },
                    model: {
                      value: _vm.unsortedAgents,
                      callback: function($$v) {
                        _vm.unsortedAgents = $$v
                      },
                      expression: "unsortedAgents"
                    }
                  },
                  _vm._l(_vm.unsortedAgents, function(item) {
                    return _c(
                      "div",
                      {
                        staticClass: "activity-agent",
                        class: item.id === _vm.activityId ? "active-agent" : ""
                      },
                      [
                        _c("i", { staticClass: "fas fa-arrows" }),
                        _vm._v(" "),
                        _c("span", [_vm._v(_vm._s(item.name))]),
                        _vm._v(" "),
                        _c("span", [_vm._v(_vm._s(item.order))])
                      ]
                    )
                  }),
                  0
                )
              ],
              1
            )
          ]
        : _vm._e(),
      _vm._v(" "),
      _c("div", { staticClass: "attribution-save" }, [
        _c(
          "span",
          { staticClass: "btn btn-primary", on: { click: _vm.saveChanges } },
          [
            _c("i", { staticClass: "fas fa-save" }),
            _vm._v("\n            Save changes\n        ")
          ]
        ),
        _vm._v(" "),
        _c(
          "span",
          {
            staticClass: "btn btn-primary",
            on: {
              click: function($event) {
                return _vm.$emit("toggle-edit")
              }
            }
          },
          [
            _c("i", { staticClass: "fas fa-times" }),
            _vm._v("\n            Cancel\n        ")
          ]
        )
      ])
    ],
    2
  )
}
var staticRenderFns = [
  function() {
    var _vm = this
    var _h = _vm.$createElement
    var _c = _vm._self._c || _h
    return _c("div", [_c("b", [_vm._v("Ordered contributors")])])
  },
  function() {
    var _vm = this
    var _h = _vm.$createElement
    var _c = _vm._self._c || _h
    return _c("div", { staticClass: "help-icon" }, [
      _c("i", { staticClass: "fas fa-question-circle" }),
      _vm._v(" "),
      _c("div", { staticClass: "help-tooltip", attrs: { role: "tooltip" } }, [
        _vm._v(
          "\n                    Contributors that should be listed in a particular order when citing.\n                "
        )
      ])
    ])
  },
  function() {
    var _vm = this
    var _h = _vm.$createElement
    var _c = _vm._self._c || _h
    return _c("div", [_c("b", [_vm._v("Unordered contributors")])])
  },
  function() {
    var _vm = this
    var _h = _vm.$createElement
    var _c = _vm._self._c || _h
    return _c("div", { staticClass: "help-icon" }, [
      _c("i", { staticClass: "fas fa-question-circle" }),
      _vm._v(" "),
      _c("div", { staticClass: "help-tooltip", attrs: { role: "tooltip" } }, [
        _vm._v(
          "\n                    Contributors that do not have to be listed in any particular order. These will be listed\n                    "
        ),
        _c("em", [_vm._v("after")]),
        _vm._v(" the ordered contributors.\n                ")
      ])
    ])
  }
]
render._withStripped = true


// CONCATENATED MODULE: ./src/components/EditActivity.vue?vue&type=template&id=dbad2a2e&

// EXTERNAL MODULE: ./node_modules/vuex/dist/vuex.esm.js
var vuex_esm = __webpack_require__(3);

// CONCATENATED MODULE: ./node_modules/vue-loader/lib/loaders/templateLoader.js??vue-loader-options!./node_modules/vue-loader/lib??vue-loader-options!./src/components/fields/DateField.vue?vue&type=template&id=374751f4&
var DateFieldvue_type_template_id_374751f4_render = function() {
  var _vm = this
  var _h = _vm.$createElement
  var _c = _vm._self._c || _h
  return _c("div", { class: _vm.classes }, [
    _c("label", { attrs: { for: _vm.fieldId } }, [_vm._t("default")], 2),
    _vm._v(" "),
    _c("input", {
      attrs: { type: "date", id: _vm.fieldId, placeholder: _vm.placeholder },
      domProps: { value: _vm.dateOnly },
      on: { change: _vm.setValue }
    })
  ])
}
var DateFieldvue_type_template_id_374751f4_staticRenderFns = []
DateFieldvue_type_template_id_374751f4_render._withStripped = true


// CONCATENATED MODULE: ./src/components/fields/DateField.vue?vue&type=template&id=374751f4&

// EXTERNAL MODULE: ./src/components/fields/Field.vue + 4 modules
var Field = __webpack_require__(13);

// CONCATENATED MODULE: ./node_modules/babel-loader/lib!./node_modules/vue-loader/lib??vue-loader-options!./src/components/fields/DateField.vue?vue&type=script&lang=js&
//
//
//
//
//
//
//
//
//
/* harmony default export */ var DateFieldvue_type_script_lang_js_ = ({name:"DateField",extends:Field["a" /* default */],props:["placeholder"],computed:{dateOnly:function dateOnly(){if(this.value)try{var a=new Date(this.value);return a.toISOString().split("T")[0]}catch(a){return this.value}}}});
// CONCATENATED MODULE: ./src/components/fields/DateField.vue?vue&type=script&lang=js&
 /* harmony default export */ var fields_DateFieldvue_type_script_lang_js_ = (DateFieldvue_type_script_lang_js_); 
// EXTERNAL MODULE: ./node_modules/vue-loader/lib/runtime/componentNormalizer.js
var componentNormalizer = __webpack_require__(1);

// CONCATENATED MODULE: ./src/components/fields/DateField.vue





/* normalize component */

var component = Object(componentNormalizer["a" /* default */])(
  fields_DateFieldvue_type_script_lang_js_,
  DateFieldvue_type_template_id_374751f4_render,
  DateFieldvue_type_template_id_374751f4_staticRenderFns,
  false,
  null,
  null,
  null
  
)

/* hot reload */
if (false) { var api; }
component.options.__file = "src/components/fields/DateField.vue"
/* harmony default export */ var DateField = (component.exports);
// EXTERNAL MODULE: ./src/components/Common.vue + 5 modules
var Common = __webpack_require__(25);

// EXTERNAL MODULE: ./src/models/activity.js
var models_activity = __webpack_require__(12);

// CONCATENATED MODULE: ./node_modules/babel-loader/lib!./node_modules/vue-loader/lib??vue-loader-options!./src/components/EditActivity.vue?vue&type=script&lang=js&
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
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
//
var draggable=function(){return Promise.resolve(/* import() */).then(__webpack_require__.t.bind(null, 37, 7))};/* harmony default export */ var EditActivityvue_type_script_lang_js_ = ({name:"EditActivity",extends:Common["a" /* default */],props:["activityId"],components:{draggable:draggable,datefield:DateField},data:function data(){return{edits:{},activityOptions:[],sortedAgents:[],unsortedAgents:[],expand:!1}},computed:_objectSpread(_objectSpread({},Object(vuex_esm["e" /* mapState */])(["controlledLists","packageId"])),{},{activity:function activity(){return models_activity["a" /* default */].query()["with"]("meta")["with"]("agent").find(this.activityId)},contributor:function contributor(){return this.activity.agent}}),methods:{getAgents:function getAgents(a){this.$set(this.edits,"activity",a);var b=models_activity["a" /* default */].query()["with"]("agent").where("activity",this.edits.activity).orderBy(function(b){return b.order}).get().map(function(b){return{name:b.agent.displayName,id:b.id,order:b.order}});this.sortedAgents=b.filter(function(b){return null!==b.order}),this.unsortedAgents=b.filter(function(b){return null===b.order}),this.activity.activity!==this.edits.activity&&this.unsortedAgents.push({name:this.contributor.displayName,id:null,order:null})},getOptions:function getOptions(b){var c=this;// this needs to be returned as a promise rather than using a computed property, because
// the options on the select field need to be changed *before* the value is changed
return new Promise(function(a){b||(c.activityOptions=[],a());var d=c.contributor.activities.filter(function(d){return d.id!==c.activityId&&d.scheme===b}).map(function(b){return b.activity});c.activityOptions=c.controlledLists.activityTypes[b].filter(function(b){return!d.includes(b.name)}),a()})},updateOrder:function updateOrder(){var b=this;this.sortedAgents=this.sortedAgents.map(function(c,a){return c.order=a+1,c.id===b.activityId&&b.$set(b.edits,"order",a+1),c}),this.unsortedAgents=this.unsortedAgents.map(function(c){return c.order=null,c.id===b.activityId&&b.$set(b.edits,"order",null),c})},saveChanges:function saveChanges(){var a=this,b=[models_activity["a" /* default */].update({where:this.activityId,data:this.edits}).then(function(){return models_activity["a" /* default */].updateMeta(a.activityId,{is_dirty:!0,is_editing:!1})})];return this.sortedAgents.concat(this.unsortedAgents).forEach(function(c){c.id&&b.push(models_activity["a" /* default */].update({where:c.id,data:{order:c.order}}).then(function(){return models_activity["a" /* default */].updateMeta(c.id,{is_dirty:!0})}))}),Promise.all(b).then(function(){a.$emit("toggle-edit")})["catch"](function(a){return console.error(a)})},refresh:function refresh(){var a=this;this.getOptions(this.activity.scheme).then(function(){a.edits=a.activity.getCopy(),a.edits.activity&&a.getAgents(a.edits.activity)})}},created:function created(){this.refresh()},watch:{activityId:function activityId(){this.refresh()}}});
// CONCATENATED MODULE: ./src/components/EditActivity.vue?vue&type=script&lang=js&
 /* harmony default export */ var components_EditActivityvue_type_script_lang_js_ = (EditActivityvue_type_script_lang_js_); 
// CONCATENATED MODULE: ./src/components/EditActivity.vue





/* normalize component */

var EditActivity_component = Object(componentNormalizer["a" /* default */])(
  components_EditActivityvue_type_script_lang_js_,
  render,
  staticRenderFns,
  false,
  null,
  null,
  null
  
)

/* hot reload */
if (false) { var EditActivity_api; }
EditActivity_component.options.__file = "src/components/EditActivity.vue"
/* harmony default export */ var EditActivity = __webpack_exports__["default"] = (EditActivity_component.exports);

/***/ })

}]);