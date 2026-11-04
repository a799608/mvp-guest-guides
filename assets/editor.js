(function(){
  var editing = false;
  var positions = [];
  var script = document.createElement("script");
  script.src = "https://cdn.jsdelivr.net/npm/interactjs/dist/interact.min.js";
  document.head.appendChild(script);

  var btn = document.createElement("button");
  btn.textContent = "\u270f Edit Layout";
  btn.style.cssText = "position:fixed;top:12px;right:12px;z-index:9999;padding:10px 20px;border-radius:8px;border:2px solid #C8990A;background:#0d2e10;color:#fff;font-weight:700;font-size:.85rem;cursor:pointer;box-shadow:0 4px 12px rgba(0,0,0,.3)";
  document.body.appendChild(btn);

  var saveBtn = document.createElement("button");
  saveBtn.textContent = "Save Layout";
  saveBtn.style.cssText = "position:fixed;top:12px;right:170px;z-index:9999;padding:10px 20px;border-radius:8px;border:2px solid #C8990A;background:#C8990A;color:#fff;font-weight:700;font-size:.85rem;cursor:pointer;box-shadow:0 4px 12px rgba(0,0,0,.3);display:none";
  document.body.appendChild(saveBtn);

  var bar = document.createElement("div");
  bar.style.cssText = "position:fixed;bottom:0;left:0;right:0;z-index:9999;background:#0d2e10;color:#fff;padding:8px 16px;font-size:.8rem;text-align:center;display:none";
  document.body.appendChild(bar);

  function getLayout(){
    var data = [];
    document.querySelectorAll(".pill").forEach(function(p){
      var h = p.querySelector(".pill-header");
      data.push({
        name: h ? h.textContent.trim() : "?",
        left: parseInt(p.style.left) || 0,
        top: parseInt(p.style.top) || 0,
        width: parseInt(p.style.width) || p.offsetWidth,
        height: parseInt(p.style.height) || p.offsetHeight
      });
    });
    return data;
  }

  function enableEdit(){
    if(typeof interact==="undefined"){
      bar.style.display="block";
      bar.textContent="Loading library... click Edit Layout again in 2 seconds.";
      return;
    }
    editing=true;
    btn.textContent="\u274c Exit Edit";
    btn.style.background="#c0392b";
    btn.style.borderColor="#c0392b";
    saveBtn.style.display="block";
    bar.style.display="block";
    bar.textContent="EDIT MODE: Drag to move. Drag edges to resize. Click Save when done.";

    var canvas=document.querySelector(".canvas");
    var pills=document.querySelectorAll(".pill");
    var cr=canvas.getBoundingClientRect();

    positions=[];
    pills.forEach(function(pill){
      var r=pill.getBoundingClientRect();
      positions.push({el:pill,left:Math.round(r.left-cr.left),top:Math.round(r.top-cr.top),width:Math.round(r.width),height:Math.round(r.height)});
    });

    canvas.style.position="relative";
    canvas.style.columnCount="auto";
    canvas.style.display="block";
    canvas.style.minHeight=Math.round(cr.height)+"px";

    positions.forEach(function(p){
      p.el.style.position="absolute";
      p.el.style.left=p.left+"px";
      p.el.style.top=p.top+"px";
      p.el.style.width=p.width+"px";
      p.el.style.height=p.height+"px";
      p.el.style.outline="2px dashed rgba(200,153,10,.5)";
      p.el.style.cursor="move";
      p.el.style.boxSizing="border-box";
      p.el.dataset.x=p.left;
      p.el.dataset.y=p.top;
      p.el.classList.add("pill-editable");
    });

    interact(".pill-editable").draggable({
      listeners:{
        move:function(e){
          var t=e.target;
          var x=(parseFloat(t.dataset.x)||0)+e.dx;
          var y=(parseFloat(t.dataset.y)||0)+e.dy;
          t.style.left=Math.round(x)+"px";
          t.style.top=Math.round(y)+"px";
          t.dataset.x=x;t.dataset.y=y;
          t.style.zIndex="100";
          var h=t.querySelector(".pill-header");
          bar.textContent=(h?h.textContent.trim():"")+" | "+t.style.width+" x "+t.style.height+" at ("+t.style.left+", "+t.style.top+")";
        },
        end:function(e){e.target.style.zIndex="1";}
      },
      autoScroll:true
    }).resizable({
      edges:{left:true,right:true,bottom:true,top:true},
      listeners:{
        move:function(e){
          var t=e.target;
          var x=(parseFloat(t.dataset.x)||0)+e.deltaRect.left;
          var y=(parseFloat(t.dataset.y)||0)+e.deltaRect.top;
          t.style.width=Math.round(e.rect.width)+"px";
          t.style.height=Math.round(e.rect.height)+"px";
          t.style.left=Math.round(x)+"px";
          t.style.top=Math.round(y)+"px";
          t.dataset.x=x;t.dataset.y=y;
          var h=t.querySelector(".pill-header");
          bar.textContent=(h?h.textContent.trim():"")+" | "+t.style.width+" x "+t.style.height+" at ("+t.style.left+", "+t.style.top+")";
        }
      },
      modifiers:[interact.modifiers.restrictSize({min:{width:80,height:40}})]
    });

    var style=document.createElement("style");
    style.id="editor-style";
    style.textContent=".pill-editable:hover{outline:2px solid #C8990A !important;z-index:50}";
    document.head.appendChild(style);
  }

  function disableEdit(){
    editing=false;
    btn.textContent="\u270f Edit Layout";
    btn.style.background="#0d2e10";
    btn.style.borderColor="#C8990A";
    saveBtn.style.display="none";
    bar.style.display="none";
    if(typeof interact!=="undefined") interact(".pill-editable").unset();
    document.querySelectorAll(".pill").forEach(function(p){
      p.style.outline="";p.style.cursor="";p.style.zIndex="";
      p.classList.remove("pill-editable");
    });
    var es=document.getElementById("editor-style");
    if(es) es.remove();
  }

  btn.addEventListener("click",function(){editing?disableEdit():enableEdit();});

  saveBtn.addEventListener("click",function(){
    var data=getLayout();
    var page=window.location.pathname.split("/").filter(Boolean)[0]||"petrarch";
    bar.textContent="Saving...";
    fetch("/save-layout",{
      method:"POST",
      headers:{"Content-Type":"application/json"},
      body:JSON.stringify({page:page,pills:data})
    }).then(function(r){return r.json();}).then(function(d){
      bar.textContent="Saved "+d.saved+" pills to file.";
      bar.style.background="#1F6224";
      setTimeout(function(){bar.style.background="#0d2e10";bar.textContent="EDIT MODE active";},3000);
    }).catch(function(e){
      bar.textContent="Save failed: "+e.message;
      bar.style.background="#c0392b";
    });
  });
})();
