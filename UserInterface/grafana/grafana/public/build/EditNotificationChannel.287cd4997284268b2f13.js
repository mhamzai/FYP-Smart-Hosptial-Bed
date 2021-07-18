(window.webpackJsonp=window.webpackJsonp||[]).push([[27],{"0Tfw":function(e,t,n){"use strict";var r,i=n("q1tI"),s=n("vF1F"),a=n("kDLi"),c=n("nKUr");function o(){return(o=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var r in n)Object.prototype.hasOwnProperty.call(n,r)&&(e[r]=n[r])}return e}).apply(this,arguments)}const l=({currentFormValues:e,imageRendererAvailable:t,register:n})=>Object(c.jsxs)(a.CollapsableSection,{label:"Notification settings",isOpen:!1,children:[Object(c.jsx)(a.Field,{children:Object(c.jsx)(a.Checkbox,o({},n("isDefault"),{label:"Default",description:"Use this notification for all alerts"}))}),Object(c.jsx)(a.Field,{children:Object(c.jsx)(a.Checkbox,o({},n("settings.uploadImage"),{label:"Include image",description:"Captures an image and include it in the notification"}))}),e.uploadImage&&!t&&(r||(r=Object(c.jsx)(a.InfoBox,{title:"No image renderer available/installed",children:"Grafana cannot find an image renderer to capture an image for the notification. Please make sure the Grafana Image Renderer plugin is installed. Please contact your Grafana administrator to install the plugin."}))),Object(c.jsx)(a.Field,{children:Object(c.jsx)(a.Checkbox,o({},n("disableResolveMessage"),{label:"Disable Resolve Message",description:"Disable the resolve message [OK] that is sent when alerting state returns to false"}))}),Object(c.jsx)(a.Field,{children:Object(c.jsx)(a.Checkbox,o({},n("sendReminder"),{label:"Send reminders",description:"Send additional notifications for triggered alerts"}))}),e.sendReminder&&Object(c.jsx)(c.Fragment,{children:Object(c.jsx)(a.Field,{label:"Send reminder every",description:"Specify how often reminders should be sent, e.g. every 30s, 1m, 10m, 30m', or 1h etc. Alert reminders are sent after rules are evaluated. A reminder can never be sent more frequently than a configured alert rule evaluation interval.",children:Object(c.jsx)(a.Input,o({},n("frequency"),{width:8}))})})]});function u(){return(u=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var r in n)Object.prototype.hasOwnProperty.call(n,r)&&(e[r]=n[r])}return e}).apply(this,arguments)}const d=({control:e,option:t,register:n,invalid:r})=>{const i=t.secure?"secureSettings."+t.propertyName:"settings."+t.propertyName;switch(t.element){case"input":return Object(c.jsx)(a.Input,u({},n(""+i,{required:!!t.required&&"Required",validate:e=>""===t.validationRule||p(e,t.validationRule)}),{invalid:r,type:t.inputType,placeholder:t.placeholder}));case"select":return Object(c.jsx)(a.InputControl,{control:e,name:""+i,render:e=>{var n;let{}=e,i=function(e,t){if(null==e)return{};var n,r,i={},s=Object.keys(e);for(r=0;r<s.length;r++)n=s[r],t.indexOf(n)>=0||(i[n]=e[n]);return i}(e.field,["ref"]);return Object(c.jsx)(a.Select,u({},i,{options:null!==(n=t.selectOptions)&&void 0!==n?n:void 0,invalid:r}))}});case"textarea":return Object(c.jsx)(a.TextArea,u({invalid:r},n(""+i,{required:!!t.required&&"Required",validate:e=>""===t.validationRule||p(e,t.validationRule)})));default:return console.error("Element not supported",t.element),null}},p=(e,t)=>!!RegExp(t).test(e)||"Invalid format";function f(){return(f=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var r in n)Object.prototype.hasOwnProperty.call(n,r)&&(e[r]=n[r])}return e}).apply(this,arguments)}const h=({control:e,currentFormValues:t,errors:n,selectedChannelOptions:r,register:i,onResetSecureField:s,secureFields:o})=>Object(c.jsx)(c.Fragment,{children:r.map((r,l)=>{var u;const p=`${r.label}-${l}`,h=t["settings."+r.showWhen.field]&&t["settings."+r.showWhen.field].value;return r.showWhen.field&&h!==r.showWhen.is?null:"checkbox"===r.element?Object(c.jsx)(a.Field,{children:Object(c.jsx)(a.Checkbox,f({},i(r.secure?"secureSettings."+r.propertyName:"settings."+r.propertyName),{label:r.label,description:r.description}))},p):Object(c.jsx)(a.Field,{label:r.label,description:r.description,invalid:n.settings&&!!n.settings[r.propertyName],error:n.settings&&(null===(u=n.settings[r.propertyName])||void 0===u?void 0:u.message),children:o&&o[r.propertyName]?Object(c.jsx)(a.Input,{readOnly:!0,value:"Configured",suffix:Object(c.jsx)(a.Button,{onClick:()=>s(r.propertyName),fill:"text",type:"button",size:"sm",children:"Clear"})}):Object(c.jsx)(d,{option:r,register:i,control:e})},p)})});function b(){return(b=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var r in n)Object.prototype.hasOwnProperty.call(n,r)&&(e[r]=n[r])}return e}).apply(this,arguments)}const j=({control:e,currentFormValues:t,errors:n,secureFields:r,selectedChannel:i,channels:s,register:o,resetSecureField:l})=>Object(c.jsxs)(c.Fragment,{children:[Object(c.jsx)(a.Field,{label:"Name",invalid:!!n.name,error:n.name&&n.name.message,children:Object(c.jsx)(a.Input,b({},o("name",{required:"Name is required"})))}),Object(c.jsx)(a.Field,{label:"Type",children:Object(c.jsx)(a.InputControl,{name:"type",render:e=>{let{}=e,t=function(e,t){if(null==e)return{};var n,r,i={},s=Object.keys(e);for(r=0;r<s.length;r++)n=s[r],t.indexOf(n)>=0||(i[n]=e[n]);return i}(e.field,["ref"]);return Object(c.jsx)(a.Select,b({},t,{options:s}))},control:e,rules:{required:!0}})}),Object(c.jsx)(h,{selectedChannelOptions:i.options.filter(e=>e.required),currentFormValues:t,secureFields:r,onResetSecureField:l,register:o,errors:n,control:e})]}),g=({control:e,currentFormValues:t,errors:n,selectedChannel:r,secureFields:i,register:s,resetSecureField:o})=>{var l;return Object(c.jsxs)(a.CollapsableSection,{label:"Optional "+r.heading,isOpen:!1,children:[""!==r.info&&Object(c.jsx)(a.Alert,{severity:"info",title:null!==(l=r.info)&&void 0!==l?l:""}),Object(c.jsx)(h,{selectedChannelOptions:r.options.filter(e=>!e.required),currentFormValues:t,register:s,errors:n,control:e,onResetSecureField:o,secureFields:i})]})};var O,v,m,y=n("ZFWI");n.d(t,"a",(function(){return x}));const x=({control:e,errors:t,selectedChannel:n,selectableChannels:r,register:s,watch:o,getValues:u,imageRendererAvailable:d,onTestChannel:p,resetSecureField:f,secureFields:h})=>{const b=C(Object(a.useTheme)());Object(i.useEffect)(()=>{const e=new Set(null==n?void 0:n.options.filter(e=>e.showWhen.field).map(e=>"settings."+e.showWhen.field))||[];o(["type","sendReminder","uploadImage",...e])},[null==n?void 0:n.options,o]);const x=u();return n?Object(c.jsxs)("div",{className:b.formContainer,children:[Object(c.jsx)("div",{className:b.formItem,children:Object(c.jsx)(j,{selectedChannel:n,channels:r,secureFields:h,resetSecureField:f,currentFormValues:x,register:s,errors:t,control:e})}),n.options.filter(e=>!e.required).length>0&&Object(c.jsx)("div",{className:b.formItem,children:Object(c.jsx)(g,{selectedChannel:n,secureFields:h,resetSecureField:f,currentFormValues:x,register:s,errors:t,control:e})}),Object(c.jsx)("div",{className:b.formItem,children:Object(c.jsx)(l,{imageRendererAvailable:d,currentFormValues:x,register:s,errors:t,control:e})}),Object(c.jsx)("div",{className:b.formButtons,children:Object(c.jsxs)(a.HorizontalGroup,{children:[v||(v=Object(c.jsx)(a.Button,{type:"submit",children:"Save"})),Object(c.jsx)(a.Button,{type:"button",variant:"secondary",onClick:()=>p(u()),children:"Test"}),Object(c.jsx)("a",{href:y.b.appSubUrl+"/alerting/notifications",children:m||(m=Object(c.jsx)(a.Button,{type:"button",variant:"secondary",children:"Back"}))})]})})]}):O||(O=Object(c.jsx)(a.Spinner,{}))},C=Object(a.stylesFactory)(e=>({formContainer:s.css``,formItem:s.css`
      flex-grow: 1;
      padding-top: ${e.spacing.md};
    `,formButtons:s.css`
      padding-top: ${e.spacing.xl};
    `}))},"4vLh":function(e,t,n){"use strict";n.d(t,"b",(function(){return o})),n.d(t,"f",(function(){return l})),n.d(t,"a",(function(){return u})),n.d(t,"g",(function(){return d})),n.d(t,"e",(function(){return p})),n.d(t,"d",(function(){return f})),n.d(t,"c",(function(){return h}));var r=n("Obii"),i=n("t8hP"),s=n("HJRA"),a=n("qOGI");function c(){return(c=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var r in n)Object.prototype.hasOwnProperty.call(n,r)&&(e[r]=n[r])}return e}).apply(this,arguments)}function o(e){return async t=>{t(Object(a.b)());const n=await Object(i.getBackendSrv)().get("/api/alerts",e);t(Object(a.c)(n))}}function l(e,t){return async n=>{await Object(i.getBackendSrv)().post(`/api/alerts/${e}/pause`,t);n(o({state:(i.locationService.getSearchObject().state||"all").toString()}))}}function u(e){return async t=>{try{await Object(i.getBackendSrv)().post("/api/alert-notifications",e),s.a.emit(r.AppEvents.alertSuccess,["Notification created"]),i.locationService.push("/alerting/notifications")}catch(e){s.a.emit(r.AppEvents.alertError,[e.data.error])}}}function d(e){return async t=>{try{await Object(i.getBackendSrv)().put("/api/alert-notifications/"+e.id,e),s.a.emit(r.AppEvents.alertSuccess,["Notification updated"])}catch(e){s.a.emit(r.AppEvents.alertError,[e.data.error])}}}function p(e){return async(t,n)=>{const r=n().notificationChannel.notificationChannel;await Object(i.getBackendSrv)().post("/api/alert-notifications/test",c({id:r.id},e))}}function f(){return async e=>{const t=(await Object(i.getBackendSrv)().get("/api/alert-notifiers")).sort((e,t)=>e.name>t.name?1:-1);e(Object(a.f)(t))}}function h(e){return async t=>{await t(f());const n=await Object(i.getBackendSrv)().get("/api/alert-notifications/"+e);t(Object(a.d)(n))}}},R1i3:function(e,t,n){"use strict";n.r(t),n.d(t,"EditNotificationChannelPage",(function(){return g}));var r,i,s=n("q1tI"),a=n("t8hP"),c=n("kDLi"),o=n("ZGyg"),l=n("hBny"),u=n("0Tfw"),d=n("4vLh"),p=n("lzJ5"),f=n("gKHt"),h=n("qOGI"),b=n("nKUr");function j(){return(j=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var r in n)Object.prototype.hasOwnProperty.call(n,r)&&(e[r]=n[r])}return e}).apply(this,arguments)}class g extends s.PureComponent{constructor(...e){super(...e),this.onSubmit=e=>{const{notificationChannel:t}=this.props;this.props.updateNotificationChannel(j({},Object(f.c)(j({},t,e,{settings:j({},t.settings,e.settings)})),{id:t.id}))},this.onTestChannel=e=>{const{notificationChannel:t}=this.props;this.props.testNotificationChannel(Object(f.d)(j({},t,e,{settings:j({},t.settings,e.settings)})))}}componentDidMount(){this.props.loadNotificationChannel(parseInt(this.props.match.params.id,10))}render(){const{navModel:e,notificationChannel:t,notificationChannelTypes:n}=this.props;return Object(b.jsx)(o.a,{navModel:e,children:Object(b.jsxs)(o.a.Contents,{children:[r||(r=Object(b.jsx)("h2",{className:"page-sub-heading",children:"Edit notification channel"})),t&&t.id>0?Object(b.jsx)(c.Form,{maxWidth:600,onSubmit:this.onSubmit,defaultValues:j({},t,{type:n.find(e=>e.value===t.type)}),children:({control:e,errors:r,getValues:i,register:s,watch:c})=>{const o=n.find(e=>e.value===i().type.value);return Object(b.jsx)(u.a,{selectableChannels:Object(f.b)(n,!0),selectedChannel:o,imageRendererAvailable:a.config.rendererAvailable,onTestChannel:this.onTestChannel,register:s,watch:c,errors:r,getValues:i,control:e,resetSecureField:this.props.resetSecureField,secureFields:t.secureFields})}}):i||(i=Object(b.jsxs)("div",{children:["Loading notification channel",Object(b.jsx)(c.Spinner,{})]}))]})})}}const O={loadNotificationChannel:d.c,testNotificationChannel:d.e,updateNotificationChannel:d.g,resetSecureField:h.e};t.default=Object(l.a)(e=>({navModel:Object(p.a)(e.navIndex,"channels"),notificationChannel:e.notificationChannel.notificationChannel,notificationChannelTypes:e.notificationChannel.notificationChannelTypes}),O,e=>e.notificationChannel)(g)},gKHt:function(e,t,n){"use strict";n.d(t,"a",(function(){return s})),n.d(t,"b",(function(){return a})),n.d(t,"c",(function(){return c})),n.d(t,"d",(function(){return o}));var r=n("Wwog");function i(){return(i=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var r in n)Object.prototype.hasOwnProperty.call(n,r)&&(e[r]=n[r])}return e}).apply(this,arguments)}const s={id:-1,name:"",type:{value:"email",label:"Email"},sendReminder:!1,disableResolveMessage:!1,frequency:"15m",settings:{uploadImage:n("t8hP").config.rendererAvailable,autoResolve:!0,httpMethod:"POST",severity:"critical"},secureSettings:{},secureFields:{},isDefault:!1},a=Object(r.default)((e,t)=>e.map(e=>t?{value:e.value,label:e.label,description:e.description}:{value:e.value,label:e.label})),c=e=>{const t=Object.fromEntries(Object.entries(e.settings).map(([e,t])=>[e,t&&t.hasOwnProperty("value")?t.value:t]));return i({},s,e,{frequency:""===e.frequency?s.frequency:e.frequency,type:e.type.value,settings:i({},s.settings,t),secureSettings:i({},e.secureSettings)})},o=e=>{var t;return{name:e.name,type:e.type.value,frequency:null!==(t=e.frequency)&&void 0!==t?t:s.frequency,settings:i({},Object.assign(s.settings,e.settings)),secureSettings:i({},e.secureSettings)}}},hBny:function(e,t,n){"use strict";n.d(t,"a",(function(){return u}));var r=n("/MKj"),i=n("zVNn"),s=n("q1tI"),a=n("2mql"),c=n.n(a),o=n("nKUr");function l(){return(l=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var n=arguments[t];for(var r in n)Object.prototype.hasOwnProperty.call(n,r)&&(e[r]=n[r])}return e}).apply(this,arguments)}const u=(e,t,n)=>a=>{const u=Object(r.connect)(e,t)(a),d=e=>{const t=Object(r.useDispatch)();return Object(s.useEffect)(()=>function(){t(Object(i.a)({stateSelector:n}))},[t]),Object(o.jsx)(u,l({},e))};return d.displayName=`ConnectWithCleanUp(${u.displayName})`,c()(d,a),d}}}]);
//# sourceMappingURL=EditNotificationChannel.287cd4997284268b2f13.js.map