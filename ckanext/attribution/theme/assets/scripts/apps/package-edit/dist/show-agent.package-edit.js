(window.webpackJsonppackage_edit=window.webpackJsonppackage_edit||[]).push([[6],{84:function(t,e,i){"use strict";i.r(e);var n=function(){var t=this,e=t.$createElement,i=t._self._c||e;return i("div",{class:t.blockClasses},[i("div",{staticClass:"agent-header"},[i("div",{staticClass:"agent-name"},[i("i",{staticClass:"fas agent-icon",class:t.agentTypeIcon(t.contributor.agent_type)}),t._v(" "),i("b",[t._v(t._s(t.contributor.standardisedName))])]),t._v(" "),i("div",{staticClass:"edit-icons"},[t.contributor.external_id?i("span",{staticClass:"edit-icon",attrs:{title:"Download contributor details from external source"},on:{click:function(e){return t.syncAgent(t.contributorId)}}},[i("i",{staticClass:"fas",class:t.contributor.meta.syncing?"fa-spinner fa-spin":"fa-arrow-alt-circle-down"})]):t._e(),t._v(" "),t.settings.canEdit?i("span",{staticClass:"edit-icon",attrs:{title:"Edit"},on:{click:t.startEdit}},[i("i",{staticClass:"fas fa-edit"})]):t._e(),t._v(" "),t.contributor.meta.is_temporary?t._e():i("span",{staticClass:"edit-icon",attrs:{title:"Remove this contributor"},on:{click:function(e){return t.eventBus.$emit(t.events.removeContributor,t.contributorId)}}},[i("i",{staticClass:"fas fa-minus-circle"})])])]),t._v(" "),i("div",{staticClass:"agent-identifier"},[t.contributor.external_id?i("a",{attrs:{href:t.contributor.externalIdUrl}},[i("i",{class:t.agentIdIcon(t.contributor.external_id_scheme)}),t._v(" "+t._s(t.contributor.external_id)+"\n        ")]):t._e(),t._v(" "),t.contributor.user_id?i("a",{attrs:{href:"/user/"+t.contributor.user_id,target:"_blank"}},[i("i",{staticClass:"far fa-smile"}),t._v(" user profile\n        ")]):t._e()]),t._v(" "),i("div",{staticClass:"agent-affiliations"},[t._l(t.affiliations.slice(0,t.affiliationLimit),(function(e){return i("span",{staticClass:"agent-affiliation"},[t._v("\n            "+t._s(e.other_agent.displayName)+" "),e.affiliation_type?[t._v("("+t._s(e.affiliation_type)+")")]:t._e()],2)})),t._v(" "),t.affiliations.length>t.affiliationLimit?i("span",{staticClass:"agent-affiliation"},[t._v("\n            "+t._s(t.affiliations.length-t.affiliationLimit)+" more\n        ")]):t._e()],2)])};n._withStripped=!0;var a=i(3),r=i(20),s=i(7);function o(t,e){var i=Object.keys(t);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(t);e&&(n=n.filter((function(e){return Object.getOwnPropertyDescriptor(t,e).enumerable}))),i.push.apply(i,n)}return i}function c(t){for(var e,i=1;i<arguments.length;i++)e=null==arguments[i]?{}:arguments[i],i%2?o(Object(e),!0).forEach((function(i){l(t,i,e[i])})):Object.getOwnPropertyDescriptors?Object.defineProperties(t,Object.getOwnPropertyDescriptors(e)):o(Object(e)).forEach((function(i){Object.defineProperty(t,i,Object.getOwnPropertyDescriptor(e,i))}));return t}function l(t,e,i){return e in t?Object.defineProperty(t,e,{value:i,enumerable:!0,configurable:!0,writable:!0}):t[e]=i,t}var f={name:"ShowAgent",extends:r.a,data:function(){return{affiliationLimit:5}},computed:c(c({},Object(a.c)(["agentIdIcon","agentTypeIcon"])),{},{affiliations:function(){return s.a.query().with("affiliations.other_agent").with("affiliations.meta").find(this.contributorId).affiliations.filter((function(t){return!t.meta.to_delete}))},blockClasses:function(){var t=["agent-detail","agent-".concat(this.contributor.agent_type.toLowerCase())];return this.contributor.meta.is_dirty&&t.push("agent-dirty"),0===this.contributor.activities.filter((function(t){return!t.meta.to_delete})).length&&t.push("agent-empty"),t}}),methods:c(c({},Object(a.b)(["syncAgent"])),{},{startEdit:function(){s.a.updateMeta(this.contributorId,{is_editing:!0})}})},u=i(1),d=Object(u.a)(f,n,[],!1,null,null,null);d.options.__file="src/components/ShowAgent.vue";e.default=d.exports}}]);