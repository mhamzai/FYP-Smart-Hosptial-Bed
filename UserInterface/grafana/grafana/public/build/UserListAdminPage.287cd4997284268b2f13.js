(window.webpackJsonp=window.webpackJsonp||[]).push([[53],{KErT:function(e,t,s){"use strict";s.r(t),function(e){var a,c,n,i,l,r,j,d,h,b=s("q1tI"),o=s("vF1F"),m=s("0cfB"),x=s("/MKj"),O=s("kDLi"),g=s("GQ3c"),u=s("ZGyg"),f=s("lzJ5"),p=s("sAJe"),N=s("rCnR"),w=s("HJRA"),A=s("EKT6"),v=s("nKUr");const y=e=>{const t="admin/users/edit/"+e.id;return Object(v.jsxs)("tr",{children:[Object(v.jsx)("td",{className:"width-4 text-center link-td",children:Object(v.jsx)("a",{href:t,children:Object(v.jsx)("img",{className:"filter-table__avatar",src:e.avatarUrl})})}),Object(v.jsx)("td",{className:"link-td max-width-10",children:Object(v.jsx)("a",{className:"ellipsis",href:t,title:e.login,children:e.login})}),Object(v.jsx)("td",{className:"link-td max-width-10",children:Object(v.jsx)("a",{className:"ellipsis",href:t,title:e.email,children:e.email})}),Object(v.jsx)("td",{className:"link-td max-width-10",children:Object(v.jsx)("a",{className:"ellipsis",href:t,title:e.name,children:e.name})}),Object(v.jsx)("td",{className:"link-td",children:e.lastSeenAtAge&&Object(v.jsx)("a",{href:t,children:e.lastSeenAtAge})}),Object(v.jsx)("td",{className:"link-td",children:e.isAdmin&&Object(v.jsx)("a",{href:t,children:d||(d=Object(v.jsx)(O.Tooltip,{placement:"top",content:"Grafana Admin",children:Object(v.jsx)(O.Icon,{name:"shield"})}))})}),Object(v.jsx)("td",{className:"text-right",children:Array.isArray(e.authLabels)&&e.authLabels.length>0&&Object(v.jsx)(N.a,{label:e.authLabels[0],removeIcon:!1,count:0})}),Object(v.jsx)("td",{className:"text-right",children:e.isDisabled&&(h||(h=Object(v.jsx)("span",{className:"label label-tag label-tag--gray",children:"Disabled"})))})]},e.id)},P=Object(O.stylesFactory)(()=>({table:o.css`
      margin-top: 28px;
    `})),L={fetchUsers:p.j,changeQuery:p.c,changePage:p.b};t.default=Object(m.hot)(e)(Object(x.connect)(e=>({navModel:Object(f.a)(e.navIndex,"global-users"),users:e.userListAdmin.users,query:e.userListAdmin.query,showPaging:e.userListAdmin.showPaging,totalPages:e.userListAdmin.totalPages,page:e.userListAdmin.page}),L)(e=>{const t=P(),{fetchUsers:s,navModel:d,query:h,changeQuery:m,users:x,showPaging:f,totalPages:p,page:N,changePage:L}=e;return Object(b.useEffect)(()=>{s()},[s]),Object(v.jsx)(u.a,{navModel:d,children:Object(v.jsx)(u.a.Contents,{children:Object(v.jsxs)(v.Fragment,{children:[Object(v.jsxs)("div",{className:"page-action-bar",children:[Object(v.jsx)("div",{className:"gf-form gf-form--grow",children:Object(v.jsx)(A.a,{placeholder:"Search user by login, email, or name.",autoFocus:!0,value:h,onChange:e=>m(e)})}),w.b.hasPermission(g.AccessControlAction.UsersCreate)&&(a||(a=Object(v.jsx)(O.LinkButton,{href:"admin/users/create",variant:"primary",children:"New user"})))]}),Object(v.jsx)("div",{className:Object(o.cx)(t.table,"admin-list-table"),children:Object(v.jsxs)("table",{className:"filter-table form-inline filter-table--hover",children:[Object(v.jsx)("thead",{children:Object(v.jsxs)("tr",{children:[c||(c=Object(v.jsx)("th",{})),n||(n=Object(v.jsx)("th",{children:"Login"})),i||(i=Object(v.jsx)("th",{children:"Email"})),l||(l=Object(v.jsx)("th",{children:"Name"})),r||(r=Object(v.jsxs)("th",{children:["Seen ",Object(v.jsx)(O.Tooltip,{placement:"top",content:"Time since user was seen using Grafana",children:Object(v.jsx)(O.Icon,{name:"question-circle"})})]})),j||(j=Object(v.jsx)("th",{})),Object(v.jsx)("th",{style:{width:"1%"}})]})}),Object(v.jsx)("tbody",{children:x.map(y)})]})}),f&&Object(v.jsx)(O.Pagination,{numberOfPages:p,currentPage:N,onNavigate:L})]})})})}))}.call(this,s("3UD+")(e))}}]);
//# sourceMappingURL=UserListAdminPage.287cd4997284268b2f13.js.map