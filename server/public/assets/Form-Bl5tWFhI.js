import{r as w,a as d,c as x,b as f,d as c,e as t,w as a,E as g,t as p,i as y,F as U,o as V,f as z,j as E,g as i}from"./index-C2VwTE3s.js";import{h as N,E as k}from"./http-K1XqM7fZ.js";import{_ as F}from"./_plugin-vue_export-helper-DlAUqK2U.js";const R={class:"buttons"},S={class:"status"},T={key:0,class:"result"},v={__name:"Form",setup(B){const e=w({btnRecordText:"开始收音",status:"",result:"",form:{xm:"",nl:"",xb:"",sfzh:"",lxfs:"",zz:"",zs:"",jws:"",grjzs:""}});d.ontext=async u=>{e.result=u,e.status="正在处理...";let l=`
    <text>${u}</text>
    请分析<text>中的内容
    以JSON的形式输出，输出的JSON遵守以下的格式：
    {
        "xm":<姓名>,
        "nl":<年龄>,
        "xb":<性别>,
        "sfzh":<身份证号>,
        "lxfs":<联系方式>,
        "zz":<症状>,
        "zs":<主诉>,
        "jws":<既往史>,
        "grjzs":<个人家族史>
    }
    如果内容中没有对应的信息，请用""代替。
    只输出JSON不要输出其他内容。
    `,s=(await N.post("/api/form",{prompt:l})).data.data.replace(/<think>[\s\S]*?<\/think>/g,"");s=s.replace("```json","").replace("```","");const r=JSON.parse(s);e.form=r,e.status=""};let m=!1;function _(){m?d.stop(()=>{i.success("停止收音"),e.status="",e.btnRecordText="开始收音",m=!1}):d.start(()=>{i.success("开始收音"),e.btnRecordText="停止收音",e.status="正在收音...",m=!0},()=>{i.error("收音错误"),e.status="",e.btnRecordText="开始收音",m=!1})}function b(){e.form={xm:"",nl:"",xb:"",sfzh:"",lxfs:"",zz:"",zs:"",jws:"",grjzs:""},e.result=""}return(u,l)=>{const n=g,s=k,r=E,j=y;return V(),x(U,null,[l[10]||(l[10]=f("div",{class:"title"},"表单填写",-1)),f("div",R,[t(n,{type:"primary",onClick:_},{default:a(()=>[z(p(e.btnRecordText),1)]),_:1}),t(n,{type:"primary",onClick:b},{default:a(()=>l[9]||(l[9]=[z("重置表单")])),_:1,__:[9]}),f("span",S,p(e.status),1)]),e.result?(V(),x("div",T,p(e.result),1)):c("",!0),t(j,{"label-width":"auto",class:"form"},{default:a(()=>[t(r,{label:"姓名"},{default:a(()=>[t(s,{modelValue:e.form.xm,"onUpdate:modelValue":l[0]||(l[0]=o=>e.form.xm=o)},null,8,["modelValue"])]),_:1}),t(r,{label:"年龄"},{default:a(()=>[t(s,{modelValue:e.form.nl,"onUpdate:modelValue":l[1]||(l[1]=o=>e.form.nl=o)},null,8,["modelValue"])]),_:1}),t(r,{label:"性别"},{default:a(()=>[t(s,{modelValue:e.form.xb,"onUpdate:modelValue":l[2]||(l[2]=o=>e.form.xb=o)},null,8,["modelValue"])]),_:1}),t(r,{label:"身份证号"},{default:a(()=>[t(s,{modelValue:e.form.sfzh,"onUpdate:modelValue":l[3]||(l[3]=o=>e.form.sfzh=o)},null,8,["modelValue"])]),_:1}),t(r,{label:"联系方式"},{default:a(()=>[t(s,{modelValue:e.form.lxfs,"onUpdate:modelValue":l[4]||(l[4]=o=>e.form.lxfs=o)},null,8,["modelValue"])]),_:1}),t(r,{label:"症状"},{default:a(()=>[t(s,{type:"textarea",rows:3,modelValue:e.form.zz,"onUpdate:modelValue":l[5]||(l[5]=o=>e.form.zz=o)},null,8,["modelValue"])]),_:1}),t(r,{label:"主诉"},{default:a(()=>[t(s,{type:"textarea",rows:3,modelValue:e.form.zs,"onUpdate:modelValue":l[6]||(l[6]=o=>e.form.zs=o)},null,8,["modelValue"])]),_:1}),t(r,{label:"既往史"},{default:a(()=>[t(s,{type:"textarea",rows:3,modelValue:e.form.jws,"onUpdate:modelValue":l[7]||(l[7]=o=>e.form.jws=o)},null,8,["modelValue"])]),_:1}),t(r,{label:"个人家族史"},{default:a(()=>[t(s,{type:"textarea",rows:3,modelValue:e.form.grjzs,"onUpdate:modelValue":l[8]||(l[8]=o=>e.form.grjzs=o)},null,8,["modelValue"])]),_:1})]),_:1})],64)}}},I=F(v,[["__scopeId","data-v-2ed70457"]]);export{I as default};
