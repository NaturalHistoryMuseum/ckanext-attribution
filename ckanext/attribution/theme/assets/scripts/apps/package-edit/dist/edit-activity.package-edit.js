(window.webpackJsonppackage_edit=window.webpackJsonppackage_edit||[]).push([[1],{67:function(t,e,i){"use strict";var s=function(){var t=this.$createElement;return(this._self._c||t)("div")};s._withStripped=!0;var n=i(23),a=i(24),r={name:"EditBase",extends:n.a,abstract:!0,props:{canSave:{default:function(){return!0}}},data:function(){return{edits:{},errors:[],showErrors:!1,loading:{},expand:!1,valid:{}}},computed:{idGen:function(){return[Object(a.a)(8)]}},methods:{saveEdit:function(){this.isValid||this.errors.push(["Not valid"])},stopEdit:function(){this.$emit(this.events.editsDone)}},watch:{errors:function(t){0===t.length&&(this.showErrors=!1)}}},o=i(2),c=Object(o.a)(r,s,[],!1,null,null,null);c.options.__file="src/components/bases/EditBase.vue";e.a=c.exports},84:function(t,e,i){"use strict";i.r(e);var s=function(){var t=this,e=t.$createElement,i=t._self._c||e;return i("div",{staticClass:"activity-edit-block"},[t.showErrors?i("Errors",{attrs:{errors:t.errors}}):t._e(),t._v(" "),i("div",{staticClass:"activity-edit-fields attribution-row"},[i("select-field",{attrs:{options:Object.keys(t.controlledLists.activityTypes)},on:{input:function(e){return t.getOptions(t.edits.scheme)}},scopedSlots:t._u([{key:"help",fn:function(){return[t._v("\n                Standardised role taxonomies like "),i("a",{attrs:{href:"http://credit.niso.org",target:"_blank"}},[t._v("CRediT")]),t._v(" and "),i("a",{attrs:{href:"https://schema.datacite.org/meta/kernel-4/include/datacite-contributorType-v4.xsd",target:"_blank"}},[t._v("DataCite's\n                contributor types")]),t._v(" enables more accurate attribution of work.\n                "),t.settings.doiPlugin?i("div",[t._v('\n                    DataCite roles will be included in the DOI metadata as "contributor type".\n                ')]):t._e()]},proxy:!0}]),model:{value:t.edits.scheme,callback:function(e){t.$set(t.edits,"scheme",e)},expression:"edits.scheme"}},[t._v("\n            Role scheme\n            ")]),t._v(" "),t.edits.scheme?i("select-field",{attrs:{options:t.activityOptions,"opt-value":function(t){return t.name},"opt-label":function(t){return t.name}},on:{input:t.getAgents},model:{value:t.edits.activity,callback:function(e){t.$set(t.edits,"activity",e)},expression:"edits.activity"}},[t._v("\n            Contribution role\n        ")]):t._e(),t._v(" "),i("select-field",{attrs:{options:t.controlledLists.activityLevels},scopedSlots:t._u([{key:"help",fn:function(){return[t._v("\n                Optional; the status of this contributor within this particular role, as defined by "),i("a",{attrs:{href:"http://credit.niso.org",target:"_blank"}},[t._v("CRediT")]),t._v(".\n            ")]},proxy:!0}]),model:{value:t.edits.level,callback:function(e){t.$set(t.edits,"level",e)},expression:"edits.level"}},[t._v("\n            Contribution level\n            ")]),t._v(" "),i("div",{staticClass:"attribution"},[i("datefield",{attrs:{placeholder:"Select date (optional)"},scopedSlots:t._u([{key:"help",fn:function(){return[t._v("\n                    Optional; can be used as a start date, or if the work only took place on a single day, etc.\n                ")]},proxy:!0}]),model:{value:t.edits.time,callback:function(e){t.$set(t.edits,"time",e)},expression:"edits.time"}},[t._v("\n                Contribution date\n                ")])],1)],1),t._v(" "),i("div",{staticClass:"expand-bar",attrs:{title:"Expand"},on:{click:function(e){t.expand=!t.expand}}},[i("i",{staticClass:"fas",class:t.expand?"fa-caret-up":"fa-caret-down"}),t._v(" "),i("small",[t._v("Advanced options")]),t._v(" "),i("i",{staticClass:"fas",class:t.expand?"fa-caret-up":"fa-caret-down"})]),t._v(" "),t.expand?[i("div",{staticClass:"activity-sorted-agents attribution-row"},[t._m(0),t._v(" "),t._m(1),t._v(" "),i("draggable",{attrs:{group:"allAgents"},on:{change:t.updateOrder},model:{value:t.sortedAgents,callback:function(e){t.sortedAgents=e},expression:"sortedAgents"}},t._l(t.sortedAgents,(function(e){return i("div",{staticClass:"activity-agent",class:e.id===t.activityId?"active-agent":""},[i("i",{staticClass:"fas fa-arrows"}),t._v(" "),i("span",[t._v(t._s(e.name))]),t._v(" "),i("span",[t._v(t._s(e.order))])])})),0)],1),t._v(" "),i("div",{staticClass:"activity-unsorted-agents attribution-row"},[t._m(2),t._v(" "),t._m(3),t._v(" "),i("draggable",{attrs:{group:"allAgents"},on:{change:t.updateOrder},model:{value:t.unsortedAgents,callback:function(e){t.unsortedAgents=e},expression:"unsortedAgents"}},t._l(t.unsortedAgents,(function(e){return i("div",{staticClass:"activity-agent",class:e.id===t.activityId?"active-agent":""},[i("i",{staticClass:"fas fa-arrows"}),t._v(" "),i("span",[t._v(t._s(e.name))]),t._v(" "),i("span",[t._v(t._s(e.order))])])})),0)],1)]:t._e(),t._v(" "),t.activity.meta.is_temporary?t._e():i("div",{staticClass:"attribution-save"},[i("span",{staticClass:"btn",class:t.isValid?"btn-primary":"btn-disabled",on:{click:t.saveEdit}},[i("i",{staticClass:"fas fa-save"}),t._v("\n            Save changes\n        ")]),t._v(" "),i("span",{staticClass:"btn btn-primary",on:{click:t.stopEdit}},[i("i",{staticClass:"fas fa-times"}),t._v("\n            Cancel\n        ")])])],2)};s._withStripped=!0;var n=i(34),a=i.n(n),r=function(){var t=this,e=t.$createElement,i=t._self._c||e;return i("div",{class:t.classes},[i("label",{attrs:{for:t.fieldId}},[t._t("default")],2),t._v(" "),t.showHelpText?i("help-tooltip",[t._t("help")],2):t._e(),t._v(" "),i("input",{staticClass:"form-control",attrs:{type:"date",id:t.fieldId,placeholder:t.placeholder},domProps:{value:t.dateOnly},on:{change:t.setValue}})],1)};r._withStripped=!0;var o={name:"DateField",extends:i(12).a,props:["placeholder"],computed:{dateOnly:function(){if(this.value)try{return new Date(this.value).toISOString().split("T")[0]}catch(t){return this.value}}}},c=i(2),d=Object(c.a)(o,r,[],!1,null,null,null);d.options.__file="src/components/fields/DateField.vue";var l=d.exports,u=i(67),v=i(10),p={name:"EditActivity",extends:u.a,props:{activityId:String},components:{draggable:a.a,datefield:l,Errors:function(){return i.e(3).then(i.bind(null,88))}},data:function(){return{activityOptions:[],sortedAgents:[],unsortedAgents:[]}},computed:{activity:function(){return v.a.query().with("meta").with("agent").find(this.activityId)},contributor:function(){return this.activity.agent},isValid:function(){return this.errors=[],this.edits.activity||this.errors.push("Activity not provided."),null!==this.edits.activity}},methods:{refresh:function(){var t=this;this.getOptions(this.activity.scheme).then((function(){t.edits=t.activity.getCopy(),t.edits.activity&&t.getAgents(t.edits.activity)})),this.$emit("validated",this.isValid)},saveEdit:function(){var t=this,e=this.isValid&&this.canSave;if(this.showErrors=!e,e){var i=[v.a.update({where:this.activityId,data:this.edits}).then((function(){return v.a.updateMeta(t.activityId,{is_dirty:!0,is_editing:!1})}))];return this.sortedAgents.concat(this.unsortedAgents).forEach((function(t){t.id&&i.push(v.a.update({where:t.id,data:{order:t.order}}).then((function(){return v.a.updateMeta(t.id,{is_dirty:!0})})))})),Promise.all(i).then((function(){t.$emit(t.events.editsSaved)})).catch((function(t){return console.error(t)})).finally((function(){t.stopEdit()}))}},getAgents:function(t){this.$set(this.edits,"activity",t);var e=v.a.query().with("agent").where("activity",this.edits.activity).orderBy((function(t){return t.order})).get().map((function(t){return{name:t.agent.displayName,id:t.id,order:t.order}}));this.sortedAgents=e.filter((function(t){return null!==t.order})),this.unsortedAgents=e.filter((function(t){return null===t.order})),this.activity.activity!==this.edits.activity&&this.unsortedAgents.push({name:this.contributor.displayName,id:null,order:null})},getOptions:function(t){var e=this;return new Promise((function(i){t||(e.activityOptions=[],i());var s=e.contributor.activities.filter((function(i){return i.id!==e.activityId&&i.scheme===t})).map((function(t){return t.activity}));e.activityOptions=e.controlledLists.activityTypes[t].filter((function(t){return!s.includes(t.name)})),i()}))},updateOrder:function(){var t=this;this.sortedAgents=this.sortedAgents.map((function(e,i){return e.order=i+1,e.id===t.activityId&&t.$set(t.edits,"order",i+1),e})),this.unsortedAgents=this.unsortedAgents.map((function(e){return e.order=null,e.id===t.activityId&&t.$set(t.edits,"order",null),e}))}},created:function(){var t=this;this.refresh(),this.eventBus.$on(this.events.saveActivity,(function(e){e===t.activityId&&t.saveEdit()}))},watch:{activityId:function(){this.refresh()}}},h=Object(c.a)(p,s,[function(){var t=this,e=t.$createElement,i=t._self._c||e;return i("div",[i("b",[t._v("Ordered contributors")])])},function(){var t=this,e=t.$createElement,i=t._self._c||e;return i("div",{staticClass:"help-icon"},[i("i",{staticClass:"fas fa-question-circle"}),t._v(" "),i("div",{staticClass:"help-tooltip",attrs:{role:"tooltip"}},[t._v("\n                    Contributors that should be listed in a particular order when citing.\n                ")])])},function(){var t=this,e=t.$createElement,i=t._self._c||e;return i("div",[i("b",[t._v("Unordered contributors")])])},function(){var t=this,e=t.$createElement,i=t._self._c||e;return i("div",{staticClass:"help-icon"},[i("i",{staticClass:"fas fa-question-circle"}),t._v(" "),i("div",{staticClass:"help-tooltip",attrs:{role:"tooltip"}},[t._v("\n                    Contributors that do not have to be listed in any particular order. These will be listed\n                    "),i("em",[t._v("after")]),t._v(" the ordered contributors.\n                ")])])}],!1,null,null,null);h.options.__file="src/components/EditActivity.vue";e.default=h.exports}}]);