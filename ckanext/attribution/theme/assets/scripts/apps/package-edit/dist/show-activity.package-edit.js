(window.webpackJsonppackage_edit=window.webpackJsonppackage_edit||[]).push([[4],{82:function(t,e,i){"use strict";i.r(e);var c=function(){var t=this,e=t.$createElement,i=t._self._c||e;return i("div",{staticClass:"agent-activity",class:[{"is-deleted":t.activity.meta.to_delete},"activity-scheme-"+t.activity.scheme]},[i("div",{staticClass:"clickable-text",class:{clicked:t.activity.meta.is_editing},on:{click:t.toggleEdit}},[i("span",[t._v(t._s(t.activity.activity))]),t._v(" "),t.activity.order?i("span",[t._v(" (#"+t._s(t.activity.order)+")")]):t._e()]),t._v(" "),i("i",{staticClass:"fas fa-sm fa-minus-circle",on:{click:function(e){return t.toggleActivity(t.activityId)}}})])};c._withStripped=!0;var r=i(5),n=i(9);function a(t,e){var i=Object.keys(t);if(Object.getOwnPropertySymbols){var c=Object.getOwnPropertySymbols(t);e&&(c=c.filter((function(e){return Object.getOwnPropertyDescriptor(t,e).enumerable}))),i.push.apply(i,c)}return i}function o(t){for(var e,i=1;i<arguments.length;i++)e=null==arguments[i]?{}:arguments[i],i%2?a(Object(e),!0).forEach((function(i){s(t,i,e[i])})):Object.getOwnPropertyDescriptors?Object.defineProperties(t,Object.getOwnPropertyDescriptors(e)):a(Object(e)).forEach((function(i){Object.defineProperty(t,i,Object.getOwnPropertyDescriptor(e,i))}));return t}function s(t,e,i){return e in t?Object.defineProperty(t,e,{value:i,enumerable:!0,configurable:!0,writable:!0}):t[e]=i,t}var l={name:"ShowActivity",props:["activityId"],data:function(){return{}},computed:{activity:function(){return n.a.query().with("meta").find(this.activityId)}},methods:o(o({},Object(r.b)(["toggleActivity"])),{},{toggleEdit:function(){this.activity.meta.to_delete&&this.toggleActivity(this.activityId),this.$emit("toggle-edit")}})},u=i(1),v=Object(u.a)(l,c,[],!1,null,null,null);v.options.__file="src/components/ShowActivity.vue";e.default=v.exports}}]);