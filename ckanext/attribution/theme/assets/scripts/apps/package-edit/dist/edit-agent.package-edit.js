(window["webpackJsonppackage_edit"] = window["webpackJsonppackage_edit"] || []).push([[1],{

/***/ 73:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// CONCATENATED MODULE: ./node_modules/vue-loader/lib/loaders/templateLoader.js??vue-loader-options!./node_modules/vue-loader/lib??vue-loader-options!./src/components/EditAgent.vue?vue&type=template&id=7717e4ca&
var render = function() {
  var _vm = this
  var _h = _vm.$createElement
  var _c = _vm._self._c || _h
  return _c(
    "div",
    {
      staticClass: "agent-edit-block agent-detail",
      class: "agent-" + _vm.edits.agent_type.toLowerCase()
    },
    [
      _c(
        "div",
        { staticClass: "agent-header" },
        [
          _c("AgentTypeField", {
            model: {
              value: _vm.edits.agent_type,
              callback: function($$v) {
                _vm.$set(_vm.edits, "agent_type", $$v)
              },
              expression: "edits.agent_type"
            }
          }),
          _vm._v(" "),
          _c("span", { staticClass: "display-name" }, [
            _c("em", [_vm._v(_vm._s(_vm.displayName))])
          ]),
          _vm._v(" "),
          _c("div", { staticClass: "edit-icons" }, [
            _vm.contributor.external_id
              ? _c(
                  "span",
                  {
                    staticClass: "edit-icon",
                    attrs: {
                      title: "Download contributor details from external source"
                    },
                    on: { click: _vm.syncAgent }
                  },
                  [
                    _c("i", {
                      staticClass: "fas",
                      class: _vm.contributor.meta.syncing
                        ? "fa-spinner fa-spin"
                        : "fa-arrow-alt-circle-down"
                    })
                  ]
                )
              : _vm._e(),
            _vm._v(" "),
            _vm.canEdit
              ? _c(
                  "span",
                  {
                    staticClass: "edit-icon",
                    attrs: { title: "Edit" },
                    on: {
                      click: function($event) {
                        return _vm.$emit("toggle-edit")
                      }
                    }
                  },
                  [_c("i", { staticClass: "fas fa-edit" })]
                )
              : _vm._e(),
            _vm._v(" "),
            _c(
              "span",
              {
                staticClass: "edit-icon",
                attrs: { title: "Remove this contributor" },
                on: {
                  click: function($event) {
                    return _vm.eventBus.$emit(
                      _vm.events.removeContributor,
                      _vm.contributorId
                    )
                  }
                }
              },
              [_c("i", { staticClass: "fas fa-minus-circle" })]
            )
          ])
        ],
        1
      ),
      _vm._v(" "),
      _c(
        "div",
        { staticClass: "agent-id-edit attribution-row" },
        [
          _c(
            "select-field",
            {
              class: ["wrap-small"],
              attrs: {
                options: Object.entries(_vm.controlledLists.agentIdSchemes),
                "opt-label": function(o) {
                  return o[1].label
                },
                "opt-value": function(o) {
                  return o[0]
                }
              },
              model: {
                value: _vm.edits.external_id_scheme,
                callback: function($$v) {
                  _vm.$set(_vm.edits, "external_id_scheme", $$v)
                },
                expression: "edits.external_id_scheme"
              }
            },
            [_vm._v("\n            External ID scheme\n        ")]
          ),
          _vm._v(" "),
          _c(
            "text-field",
            {
              class: ["wrap-small"],
              attrs: {
                placeholder:
                  _vm.controlledLists.agentIdSchemes[
                    _vm.edits.external_id_scheme
                  ].label
              },
              model: {
                value: _vm.edits.external_id,
                callback: function($$v) {
                  _vm.$set(_vm.edits, "external_id", $$v)
                },
                expression: "edits.external_id"
              }
            },
            [
              _c("i", {
                class:
                  _vm.controlledLists.agentIdSchemes[
                    _vm.edits.external_id_scheme
                  ].fa_icon
              }),
              _vm._v(
                "\n            " +
                  _vm._s(
                    _vm.controlledLists.agentIdSchemes[
                      _vm.edits.external_id_scheme
                    ].label
                  ) +
                  "\n        "
              )
            ]
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
          _c("small", [_vm._v("Show all edit options")]),
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
              { staticClass: "agent-name-edit attribution-row" },
              [
                _vm.edits.agent_type === "person"
                  ? [
                      _c(
                        "text-field",
                        {
                          attrs: { cls: ["wrap-small"] },
                          model: {
                            value: _vm.edits.family_name,
                            callback: function($$v) {
                              _vm.$set(_vm.edits, "family_name", $$v)
                            },
                            expression: "edits.family_name"
                          }
                        },
                        [
                          _vm._v(
                            "\n                    Family name\n                "
                          )
                        ]
                      ),
                      _vm._v(" "),
                      _c(
                        "text-field",
                        {
                          attrs: { cls: ["wrap-small"] },
                          model: {
                            value: _vm.edits.given_names,
                            callback: function($$v) {
                              _vm.$set(_vm.edits, "given_names", $$v)
                            },
                            expression: "edits.given_names"
                          }
                        },
                        [
                          _vm._v(
                            "\n                    Given name(s)\n                "
                          )
                        ]
                      ),
                      _vm._v(" "),
                      _vm._l(_vm.idGen, function(fieldId) {
                        return _c(
                          "div",
                          { staticClass: "attribution-field one-line" },
                          [
                            _c("label", { attrs: { for: fieldId } }, [
                              _vm._v(
                                "\n                        Given names first\n                    "
                              )
                            ]),
                            _vm._v(" "),
                            _c("input", {
                              directives: [
                                {
                                  name: "model",
                                  rawName: "v-model",
                                  value: _vm.edits.given_names_first,
                                  expression: "edits.given_names_first"
                                }
                              ],
                              attrs: { id: fieldId, type: "checkbox" },
                              domProps: {
                                checked: Array.isArray(
                                  _vm.edits.given_names_first
                                )
                                  ? _vm._i(_vm.edits.given_names_first, null) >
                                    -1
                                  : _vm.edits.given_names_first
                              },
                              on: {
                                change: function($event) {
                                  var $$a = _vm.edits.given_names_first,
                                    $$el = $event.target,
                                    $$c = $$el.checked ? true : false
                                  if (Array.isArray($$a)) {
                                    var $$v = null,
                                      $$i = _vm._i($$a, $$v)
                                    if ($$el.checked) {
                                      $$i < 0 &&
                                        _vm.$set(
                                          _vm.edits,
                                          "given_names_first",
                                          $$a.concat([$$v])
                                        )
                                    } else {
                                      $$i > -1 &&
                                        _vm.$set(
                                          _vm.edits,
                                          "given_names_first",
                                          $$a
                                            .slice(0, $$i)
                                            .concat($$a.slice($$i + 1))
                                        )
                                    }
                                  } else {
                                    _vm.$set(
                                      _vm.edits,
                                      "given_names_first",
                                      $$c
                                    )
                                  }
                                }
                              }
                            })
                          ]
                        )
                      }),
                      _vm._v(" "),
                      _c("help-tooltip", [
                        _vm._v(
                          "\n                    Does this person's culture or language typically place given or family\n                    names first? (this does not affect sorting)\n                "
                        )
                      ])
                    ]
                  : _vm._e(),
                _vm._v(" "),
                _vm.edits.agent_type !== "person"
                  ? [
                      _c(
                        "text-field",
                        {
                          model: {
                            value: _vm.edits.name,
                            callback: function($$v) {
                              _vm.$set(_vm.edits, "name", $$v)
                            },
                            expression: "edits.name"
                          }
                        },
                        [_vm._v("\n                    Name\n                ")]
                      ),
                      _vm._v(" "),
                      _c(
                        "text-field",
                        {
                          model: {
                            value: _vm.edits.location,
                            callback: function($$v) {
                              _vm.$set(_vm.edits, "location", $$v)
                            },
                            expression: "edits.location"
                          }
                        },
                        [
                          _vm._v(
                            "\n                    Location\n                "
                          )
                        ]
                      )
                    ]
                  : _vm._e()
              ],
              2
            ),
            _vm._v(" "),
            _c(
              "div",
              { staticClass: "agent-user-edit attribution-row" },
              [
                _c("autocomplete-field", {
                  attrs: {
                    options: _vm.userOptions,
                    label: "Associated user",
                    "item-id": "agent-user-" + _vm.contributorId
                  },
                  on: { typing: _vm.updateUserOptions },
                  model: {
                    value: _vm.edits.user_id,
                    callback: function($$v) {
                      _vm.$set(_vm.edits, "user_id", $$v)
                    },
                    expression: "edits.user_id"
                  }
                }),
                _vm._v(" "),
                _c("help-tooltip", [
                  _vm._v(
                    "\n                If this contributor has a user account registered on the portal, associate it here\n            "
                  )
                ])
              ],
              1
            ),
            _vm._v(" "),
            _c(
              "div",
              { staticClass: "agent-affiliations-edit attribution-row" },
              [
                _c("autocomplete-list", {
                  attrs: {
                    options: _vm.affiliationOptions,
                    label: "Add affiliation",
                    "item-id": "agent-affiliation-" + _vm.contributorId
                  },
                  on: { typing: _vm.updateAffiliationOptions },
                  model: {
                    value: _vm.affiliations,
                    callback: function($$v) {
                      _vm.affiliations = $$v
                    },
                    expression: "affiliations"
                  }
                }),
                _vm._v(" "),
                _c("help-tooltip", [
                  _vm._v(
                    "\n                For affiliations that are associated with "
                  ),
                  _c("em", [_vm._v("this package only")]),
                  _vm._v(
                    ". Only includes contributors\n                that have already been added to this page.\n            "
                  )
                ])
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
var staticRenderFns = []
render._withStripped = true


// CONCATENATED MODULE: ./src/components/EditAgent.vue?vue&type=template&id=7717e4ca&

// EXTERNAL MODULE: ./node_modules/vuex/dist/vuex.esm.js
var vuex_esm = __webpack_require__(3);

// EXTERNAL MODULE: ./src/api.js
var api = __webpack_require__(7);

// EXTERNAL MODULE: ./node_modules/nanoid/index.browser.js + 1 modules
var index_browser = __webpack_require__(34);

// EXTERNAL MODULE: ./src/components/Common.vue + 5 modules
var Common = __webpack_require__(25);

// EXTERNAL MODULE: ./src/models/main.js
var main = __webpack_require__(0);

// CONCATENATED MODULE: ./node_modules/vue-loader/lib/loaders/templateLoader.js??vue-loader-options!./node_modules/vue-loader/lib??vue-loader-options!./src/components/fields/AgentTypeField.vue?vue&type=template&id=732f0b9e&
var AgentTypeFieldvue_type_template_id_732f0b9e_render = function() {
  var _vm = this
  var _h = _vm.$createElement
  var _c = _vm._self._c || _h
  return _c(
    "div",
    { staticClass: "agent-type-edit", class: _vm.classes },
    _vm._l(_vm.options, function(info, name) {
      return _c("span", { staticClass: "agent-type-option" }, [
        _c("input", {
          attrs: { type: "radio", id: _vm.optionId(name) },
          domProps: { value: name, checked: _vm.value === name },
          on: { change: _vm.setValue }
        }),
        _vm._v(" "),
        _c("label", { attrs: { for: _vm.optionId(name) } }, [
          _c("i", { class: info.fa_icon })
        ])
      ])
    }),
    0
  )
}
var AgentTypeFieldvue_type_template_id_732f0b9e_staticRenderFns = []
AgentTypeFieldvue_type_template_id_732f0b9e_render._withStripped = true


// CONCATENATED MODULE: ./src/components/fields/AgentTypeField.vue?vue&type=template&id=732f0b9e&

// EXTERNAL MODULE: ./src/components/fields/Field.vue + 4 modules
var Field = __webpack_require__(13);

// CONCATENATED MODULE: ./node_modules/babel-loader/lib!./node_modules/vue-loader/lib??vue-loader-options!./src/components/fields/AgentTypeField.vue?vue&type=script&lang=js&
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
/* harmony default export */ var AgentTypeFieldvue_type_script_lang_js_ = ({name:"AgentTypeField",extends:Field["a" /* default */],computed:_objectSpread(_objectSpread({},Object(vuex_esm["e" /* mapState */])(["controlledLists"])),{},{options:function options(){return this.controlledLists.agentTypes}}),methods:{optionId:function optionId(a){return"agent-type-option-"+a+this.fieldId}}});
// CONCATENATED MODULE: ./src/components/fields/AgentTypeField.vue?vue&type=script&lang=js&
 /* harmony default export */ var fields_AgentTypeFieldvue_type_script_lang_js_ = (AgentTypeFieldvue_type_script_lang_js_); 
// EXTERNAL MODULE: ./node_modules/vue-loader/lib/runtime/componentNormalizer.js
var componentNormalizer = __webpack_require__(1);

// CONCATENATED MODULE: ./src/components/fields/AgentTypeField.vue





/* normalize component */

var component = Object(componentNormalizer["a" /* default */])(
  fields_AgentTypeFieldvue_type_script_lang_js_,
  AgentTypeFieldvue_type_template_id_732f0b9e_render,
  AgentTypeFieldvue_type_template_id_732f0b9e_staticRenderFns,
  false,
  null,
  null,
  null
  
)

/* hot reload */
if (false) { var AgentTypeField_api; }
component.options.__file = "src/components/fields/AgentTypeField.vue"
/* harmony default export */ var AgentTypeField = (component.exports);
// CONCATENATED MODULE: ./node_modules/babel-loader/lib!./node_modules/vue-loader/lib??vue-loader-options!./src/components/EditAgent.vue?vue&type=script&lang=js&
function EditAgentvue_type_script_lang_js_ownKeys(a,b){var c=Object.keys(a);if(Object.getOwnPropertySymbols){var d=Object.getOwnPropertySymbols(a);b&&(d=d.filter(function(b){return Object.getOwnPropertyDescriptor(a,b).enumerable})),c.push.apply(c,d)}return c}function EditAgentvue_type_script_lang_js_objectSpread(a){for(var b,c=1;c<arguments.length;c++)b=null==arguments[c]?{}:arguments[c],c%2?EditAgentvue_type_script_lang_js_ownKeys(Object(b),!0).forEach(function(c){EditAgentvue_type_script_lang_js_defineProperty(a,c,b[c])}):Object.getOwnPropertyDescriptors?Object.defineProperties(a,Object.getOwnPropertyDescriptors(b)):EditAgentvue_type_script_lang_js_ownKeys(Object(b)).forEach(function(c){Object.defineProperty(a,c,Object.getOwnPropertyDescriptor(b,c))});return a}function EditAgentvue_type_script_lang_js_defineProperty(a,b,c){return b in a?Object.defineProperty(a,b,{value:c,enumerable:!0,configurable:!0,writable:!0}):a[b]=c,a}//
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
/* harmony default export */ var EditAgentvue_type_script_lang_js_ = ({name:"EditAgent",extends:Common["a" /* default */],components:{AgentTypeField:AgentTypeField},data:function data(){return{edits:{},affiliations:[],expand:!1,userOptions:[],affiliationOptions:[],syncing:!1}},computed:EditAgentvue_type_script_lang_js_objectSpread(EditAgentvue_type_script_lang_js_objectSpread({},Object(vuex_esm["e" /* mapState */])(["canEdit","packageId","controlledLists"])),{},{contributor:function contributor(){return main["c" /* Agent */].query()["with"]("meta")["with"]("affiliations.other_agent")["with"]("affiliations.meta").find(this.contributorId)},displayName:function displayName(){return"person"===this.edits.agent_type?this.edits.given_names_first?[this.edits.given_names,this.edits.family_name].join(" "):[this.edits.family_name,this.edits.given_names].join(" "):this.edits.name},idGen:function idGen(){return[Object(index_browser["a" /* nanoid */])(8)]}}),methods:EditAgentvue_type_script_lang_js_objectSpread(EditAgentvue_type_script_lang_js_objectSpread({},Object(vuex_esm["b" /* mapActions */])(["removeContributor"])),{},{saveChanges:function saveChanges(){var b=this,c=[],d=this.affiliations.filter(function(c){return-1===b.contributor.affiliations.findIndex(function(a){return a.other_agent_id===c.value})}).map(function(d){var a={agent_id:b.contributorId,other_agent_id:d.value,package_id:b.packageId,meta:{is_new:!0}};return main["c" /* Agent */].query().where("id",d.value).exists()||(d.record.meta={is_new:!0},c.push(main["c" /* Agent */].insert({data:d.record}))),a});return c.push(main["b" /* Affiliation */].insert({data:d})),this.contributor.affiliations.filter(function(c){return-1===b.affiliations.findIndex(function(a){return a.value===c.other_agent_id})}).forEach(function(b){c.push(main["b" /* Affiliation */].updateMeta(b.id,{to_delete:!0}))}),c.push(main["c" /* Agent */].update({where:this.contributorId,data:this.edits})),Promise.all(c).then(function(){return main["c" /* Agent */].updateMeta(b.contributorId,{is_dirty:!0})}).then(function(){b.$emit("toggle-edit")})["catch"](function(a){return console.error(a)})},updateUserOptions:function updateUserOptions(a){var b=this;return""===a||null===a?void(this.userOptions=[]):void Object(api["b" /* get */])("user_list?q="+a).then(function(a){b.userOptions=a.map(function(a){return{label:a.display_name,value:a.id}})})},updateAffiliationOptions:function updateAffiliationOptions(b){var c=this,d=main["c" /* Agent */].query().where("isActive",!0).where(function(b){return b.id!==c.contributorId}).where(function(b){return-1===c.affiliations.findIndex(function(a){return a.value===b.id})});b&&""!==b&&(d=d.where(function(c){var a=b.toLowerCase(),d=!!c.family_name&&c.family_name.toLowerCase().startsWith(a),e=!!c.given_names&&c.given_names.toLowerCase().startsWith(a),f=!!c.name&&c.name.toLowerCase().startsWith(a);return d||e||f})),this.affiliationOptions=d.get().map(function(a){return{label:a.displayName,value:a.id,record:a}})},syncAgent:function syncAgent(){this.$store.dispatch("syncAgent",this.contributorId).then(this.refresh)},refresh:function refresh(){var a=this;if(this.edits=this.contributor.getCopy(),this.affiliations=this.contributor.affiliations.filter(function(b){return!b.meta.to_delete}).map(function(b){return{label:b.other_agent.displayName,value:b.other_agent_id,record:b.other_agent}}),this.edits.agent_type||this.edits.external_id_scheme||this.$set(this.edits,"agent_type",Object.keys(this.controlledLists.agentTypes)[0]),!this.edits.agent_type&&this.edits.external_id_scheme){var b=Object.entries(this.controlledLists.agentTypes).filter(function(b){return b[1]["default"]===a.edits.external_id_scheme});0<b.length&&this.$set(this.edits,"agent_type",b[0][0])}this.edits.external_id_scheme||this.$set(this.edits,"external_id_scheme",this.controlledLists.agentTypes[this.edits.agent_type].default_scheme),void 0===this.edits.given_names_first&&this.$set(this.edits,"given_names_first",!0),this.edits.user_id&&Object(api["b" /* get */])("user_show?id="+this.edits.user_id).then(function(b){a.userOptions=[{label:b.display_name,value:a.edits.user_id}]})}}),created:function created(){this.refresh()}});
// CONCATENATED MODULE: ./src/components/EditAgent.vue?vue&type=script&lang=js&
 /* harmony default export */ var components_EditAgentvue_type_script_lang_js_ = (EditAgentvue_type_script_lang_js_); 
// CONCATENATED MODULE: ./src/components/EditAgent.vue





/* normalize component */

var EditAgent_component = Object(componentNormalizer["a" /* default */])(
  components_EditAgentvue_type_script_lang_js_,
  render,
  staticRenderFns,
  false,
  null,
  null,
  null
  
)

/* hot reload */
if (false) { var EditAgent_api; }
EditAgent_component.options.__file = "src/components/EditAgent.vue"
/* harmony default export */ var EditAgent = __webpack_exports__["default"] = (EditAgent_component.exports);

/***/ })

}]);