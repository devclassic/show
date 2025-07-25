import{r as y,c as V,a as d,b as j,d as l,w as s,t as f,F as g,o as b,e as z}from"./index-CdTik-5j.js";import{E,d as U}from"./el-form-item-DfUAFrTS.js";import{E as F}from"./el-input-B0NEveY9.js";import{E as N,a as p,h as _}from"./el-message-BgJcoQvx.js";import{a as i}from"./asr-5o_LRsin.js";import{_ as k}from"./_plugin-vue_export-helper-DlAUqK2U.js";const T={class:"buttons"},v={class:"status"},R={key:0,class:"result"},S={__name:"Form",setup(B){const e=y({btnRecordText:"开始收音",status:"",result:"",form:{xm:"",nl:"",xb:"",sfzh:"",lxfs:"",zz:"",zs:"",jws:"",grjzs:""}});let u=!1;function w(){u?i.stop(async()=>{p.success("停止收音"),e.status="正在识别...",e.btnRecordText="开始收音",u=!1;const x=i.getWAVBlob(),t=new File([x],"audio.wav"),m=new FormData;m.append("file",t);let a=await _.post("/api/asr",m,{headers:{"Content-Type":"multipart/form-data"}});e.status="",e.result=a.data.data[0].text,e.status="正在处理...";const r=`
        <text>${e.result}</text>
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
        所有用到的数字都用阿拉伯数字。
        只输出JSON不要输出其他内容。
        `;a=await _.post("/api/form",{prompt:r});let n=a.data.data.replace(/<think>[\s\S]*?<\/think>/g,"");n=n.replace("```json","").replace("```","");const o=JSON.parse(n);e.form=o,e.status=""}):i.start(()=>{p.success("开始收音"),e.btnRecordText="停止收音",e.status="正在收音...",u=!0},async()=>{p.error("收音错误"),e.status="正在处理...",e.btnRecordText="开始收音",u=!1})}function c(){e.form={xm:"",nl:"",xb:"",sfzh:"",lxfs:"",zz:"",zs:"",jws:"",grjzs:""},e.result=""}return(x,t)=>{const m=N,a=F,r=U,n=E;return b(),V(g,null,[t[10]||(t[10]=d("div",{class:"title"},"表单填写",-1)),d("div",T,[l(m,{type:"primary",onClick:w},{default:s(()=>[z(f(e.btnRecordText),1)]),_:1}),l(m,{type:"primary",onClick:c},{default:s(()=>t[9]||(t[9]=[z("重置表单")])),_:1,__:[9]}),d("span",v,f(e.status),1)]),e.result?(b(),V("div",R,f(e.result),1)):j("",!0),l(n,{"label-width":"auto",class:"form"},{default:s(()=>[l(r,{label:"姓名"},{default:s(()=>[l(a,{modelValue:e.form.xm,"onUpdate:modelValue":t[0]||(t[0]=o=>e.form.xm=o)},null,8,["modelValue"])]),_:1}),l(r,{label:"年龄"},{default:s(()=>[l(a,{modelValue:e.form.nl,"onUpdate:modelValue":t[1]||(t[1]=o=>e.form.nl=o)},null,8,["modelValue"])]),_:1}),l(r,{label:"性别"},{default:s(()=>[l(a,{modelValue:e.form.xb,"onUpdate:modelValue":t[2]||(t[2]=o=>e.form.xb=o)},null,8,["modelValue"])]),_:1}),l(r,{label:"身份证号"},{default:s(()=>[l(a,{modelValue:e.form.sfzh,"onUpdate:modelValue":t[3]||(t[3]=o=>e.form.sfzh=o)},null,8,["modelValue"])]),_:1}),l(r,{label:"联系方式"},{default:s(()=>[l(a,{modelValue:e.form.lxfs,"onUpdate:modelValue":t[4]||(t[4]=o=>e.form.lxfs=o)},null,8,["modelValue"])]),_:1}),l(r,{label:"症状"},{default:s(()=>[l(a,{type:"textarea",rows:3,modelValue:e.form.zz,"onUpdate:modelValue":t[5]||(t[5]=o=>e.form.zz=o)},null,8,["modelValue"])]),_:1}),l(r,{label:"主诉"},{default:s(()=>[l(a,{type:"textarea",rows:3,modelValue:e.form.zs,"onUpdate:modelValue":t[6]||(t[6]=o=>e.form.zs=o)},null,8,["modelValue"])]),_:1}),l(r,{label:"既往史"},{default:s(()=>[l(a,{type:"textarea",rows:3,modelValue:e.form.jws,"onUpdate:modelValue":t[7]||(t[7]=o=>e.form.jws=o)},null,8,["modelValue"])]),_:1}),l(r,{label:"个人家族史"},{default:s(()=>[l(a,{type:"textarea",rows:3,modelValue:e.form.grjzs,"onUpdate:modelValue":t[8]||(t[8]=o=>e.form.grjzs=o)},null,8,["modelValue"])]),_:1})]),_:1})],64)}}},M=k(S,[["__scopeId","data-v-e2fb6b83"]]);export{M as default};
