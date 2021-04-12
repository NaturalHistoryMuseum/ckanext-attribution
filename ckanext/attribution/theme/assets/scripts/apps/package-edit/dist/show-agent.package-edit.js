(window["webpackJsonppackage_edit"] = window["webpackJsonppackage_edit"] || []).push([[4],{

/***/ 75:
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// CONCATENATED MODULE: ./node_modules/vue-loader/lib/loaders/templateLoader.js??vue-loader-options!./node_modules/vue-loader/lib??vue-loader-options!./src/components/ShowAgent.vue?vue&type=template&id=489d8208&
var render = function() {
  var _vm = this
  var _h = _vm.$createElement
  var _c = _vm._self._c || _h
  return _c("div", { class: _vm.blockClasses }, [
    _c("div", { staticClass: "agent-header" }, [
      _c("div", { staticClass: "agent-name" }, [
        _c("i", {
          staticClass: "fas agent-icon",
          class: _vm.agentTypeIcon(_vm.contributor.agent_type)
        }),
        _vm._v(" "),
        _c("b", [_vm._v(_vm._s(_vm.contributor.standardisedName))])
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
                on: {
                  click: function($event) {
                    return _vm.syncAgent(_vm.contributorId)
                  }
                }
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
    ]),
    _vm._v(" "),
    _c("div", { staticClass: "agent-identifier" }, [
      _vm.contributor.external_id
        ? _c("a", { attrs: { href: _vm.contributor.externalIdUrl } }, [
            _c("i", {
              class: _vm.agentIdIcon(_vm.contributor.external_id_scheme)
            }),
            _vm._v(" " + _vm._s(_vm.contributor.external_id) + "\n        ")
          ])
        : _vm._e(),
      _vm._v(" "),
      _vm.contributor.user_id
        ? _c(
            "a",
            {
              attrs: {
                href: "/user/" + _vm.contributor.user_id,
                target: "_blank"
              }
            },
            [
              _c("i", { staticClass: "far fa-smile" }),
              _vm._v(" user profile\n        ")
            ]
          )
        : _vm._e()
    ]),
    _vm._v(" "),
    _c(
      "div",
      { staticClass: "agent-affiliations" },
      [
        _vm._l(_vm.affiliations.slice(0, _vm.affiliationLimit), function(
          affiliation
        ) {
          return _c(
            "span",
            { staticClass: "agent-affiliation" },
            [
              _vm._v(
                "\n            " +
                  _vm._s(affiliation.other_agent.displayName) +
                  " "
              ),
              affiliation.affiliation_type
                ? [_vm._v("(" + _vm._s(affiliation.affiliation_type) + ")")]
                : _vm._e()
            ],
            2
          )
        }),
        _vm._v(" "),
        _vm.affiliations.length > _vm.affiliationLimit
          ? _c("span", { staticClass: "agent-affiliation" }, [
              _vm._v(
                "\n            " +
                  _vm._s(_vm.affiliations.length - _vm.affiliationLimit) +
                  " more\n        "
              )
            ])
          : _vm._e()
      ],
      2
    )
  ])
}
var staticRenderFns = []
render._withStripped = true


// CONCATENATED MODULE: ./src/components/ShowAgent.vue?vue&type=template&id=489d8208&

// EXTERNAL MODULE: ./node_modules/vuex/dist/vuex.esm.js
var vuex_esm = __webpack_require__(3);

// EXTERNAL MODULE: ./src/components/Common.vue + 5 modules
var Common = __webpack_require__(25);

// EXTERNAL MODULE: ./src/models/agent.js
var agent = __webpack_require__(8);

// CONCATENATED MODULE: ./node_modules/babel-loader/lib!./node_modules/vue-loader/lib??vue-loader-options!./src/components/ShowAgent.vue?vue&type=script&lang=js&
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
/* harmony default export */ var ShowAgentvue_type_script_lang_js_ = ({name:"ShowAgent",extends:Common["a" /* default */],data:function data(){return{affiliationLimit:5}},computed:_objectSpread(_objectSpread(_objectSpread({},Object(vuex_esm["e" /* mapState */])(["canEdit","controlledLists"])),Object(vuex_esm["c" /* mapGetters */])(["agentIdIcon","agentTypeIcon"])),{},{affiliations:function affiliations(){return agent["a" /* default */].query()["with"]("affiliations.other_agent")["with"]("affiliations.meta").find(this.contributorId).affiliations.filter(function(b){return!b.meta.to_delete})},blockClasses:function blockClasses(){var a=["agent-detail","agent-".concat(this.contributor.agent_type.toLowerCase())];return this.contributor.meta.is_dirty&&a.push("agent-dirty"),0===this.contributor.activities.filter(function(b){return!b.meta.to_delete}).length&&a.push("agent-empty"),a}}),methods:_objectSpread({},Object(vuex_esm["b" /* mapActions */])(["syncAgent"]))});
// CONCATENATED MODULE: ./src/components/ShowAgent.vue?vue&type=script&lang=js&
 /* harmony default export */ var components_ShowAgentvue_type_script_lang_js_ = (ShowAgentvue_type_script_lang_js_); 
// EXTERNAL MODULE: ./node_modules/vue-loader/lib/runtime/componentNormalizer.js
var componentNormalizer = __webpack_require__(1);

// CONCATENATED MODULE: ./src/components/ShowAgent.vue





/* normalize component */

var component = Object(componentNormalizer["a" /* default */])(
  components_ShowAgentvue_type_script_lang_js_,
  render,
  staticRenderFns,
  false,
  null,
  null,
  null
  
)

/* hot reload */
if (false) { var api; }
component.options.__file = "src/components/ShowAgent.vue"
/* harmony default export */ var ShowAgent = __webpack_exports__["default"] = (component.exports);

/***/ })

}]);