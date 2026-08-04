# -*- coding: utf-8 -*-
import sys
path = '/Users/subariyanto/.openclaw/workspace/aplikasi-supervisi-jatim-v4/index.html'
with open(path, 'rb') as f:
    data = f.read()
NL = '\r\n'

def rep(old, new, count=1):
    global data
    ob, nb = old.encode('utf-8'), new.encode('utf-8')
    n = data.count(ob)
    if n != count:
        print('FAIL expected %d got %d for: %r' % (count, n, old[:90]))
        sys.exit(1)
    data = data.replace(ob, nb)
    print('OK (%d): %r' % (n, old[:80]))

# ---- 1. Navbar: remove the 3 "Input ..." dropdown items (line with trailing CRLF) ----
rep("<a onclick=\"state.activeTab='kokurikuler';navigate('observasi')\" data-nav=\"observasi\">\U0001F4DD Input Kokurikuler</a>\r\n", "")
rep("<a onclick=\"state.activeTab='ekstrakurikuler';navigate('observasi')\" data-nav=\"observasi\">\U0001F4DD Input Ekstrakurikuler</a>\r\n", "")
rep("<a onclick=\"state.activeTab='iklim-madrasah';navigate('observasi')\" data-nav=\"observasi\">\U0001F4DD Input Iklim Madrasah</a>\r\n", "")

# ---- 2. Navbar: Supervisi dropdown Input item -> Daftar Supervisi (legacy list view) ----
rep("<a onclick=\"state.activeTab='supervisi';navigate('observasi')\" data-nav=\"observasi\">\U0001F4DD Input Supervisi</a>",
    "<a onclick=\"navigate('supervisi')\" data-nav=\"supervisi\">\U0001F4CB Daftar Supervisi</a>")

# ---- 3. Navbar: top-level item -> input-observasi view ----
rep("<li><span onclick=\"navigate('observasi')\" data-nav=\"observasi\">\U0001F4DD Input Observasi</span></li>",
    "<li><span onclick=\"navigate('input-observasi')\" data-nav=\"input-observasi\">\U0001F4DD Input Observasi</span></li>")

# ---- 4. render() switch case ----
rep("case 'observasi':app.innerHTML=renderObservasiPage();break;",
    "case 'input-observasi':app.innerHTML=renderInputObservasi();break;")

# ---- 5. Page title logic ----
rep("titleEl.innerHTML=state.view==='observasi'?obsTitle:",
    "titleEl.innerHTML=state.view==='input-observasi'?obsTitle:")

# ---- 6. backToDashboard ----
rep("function backToDashboard(){state.view='observasi';state.activeTab='supervisi';state.jenjang='mi';render()}",
    "function backToDashboard(){state.view='input-observasi';state.activeTab='supervisi';state.jenjang='mi';render()}")

# ---- 7. gotoObservasi ----
rep("function gotoObservasi(tab){state.view='observasi';state.activeTab=tab||state.activeTab||'supervisi';render();}",
    "function gotoObservasi(tab){state.view='input-observasi';state.activeTab=tab||state.activeTab||'supervisi';render();}")

# ---- 8. saveForm ----
rep("saveData(data);state.view='observasi';state.activeTab='supervisi';render();",
    "saveData(data);state.view='input-observasi';state.activeTab='supervisi';render();")

# ---- 9. renderObservasiPage -> renderInputObservasi ----
rep("function renderObservasiPage(){", "function renderInputObservasi(){")

# ---- 10. tab onclick -> setActiveTab ----
rep("onclick=\"setObsTab(\\'" + "'+it[0]+'" + "\\')\"", "onclick=\"setActiveTab(\\'" + "'+it[0]+'" + "\\')\"")

# ---- 11. setObsTab def -> setActiveTab ----
rep("function setObsTab(tab){state.activeTab=tab;render();}",
    "function setActiveTab(tab){state.activeTab=tab;render();}")

# ---- 13. hide Tutup buttons in list pages when inside input-observasi ----
rep("if(state.view!=='observasi'){html+='<div class=\"no-print\" style=\"margin-top:20px;text-align:right\"><button class=\"btn btn-danger\" onclick=\"navigate(\\'dashboard\\')\" style=\"padding:8px 20px\">\u2715 Tutup</button></div>';}",
    "if(state.view!=='input-observasi'){html+='<div class=\"no-print\" style=\"margin-top:20px;text-align:right\"><button class=\"btn btn-danger\" onclick=\"navigate(\\'dashboard\\')\" style=\"padding:8px 20px\">\u2715 Tutup</button></div>';}")
rep("if(state.view!=='observasi'){html+='<div class=\"no-print\" style=\"margin-top:20px;text-align:right\"><button class=\"btn btn-danger\" onclick=\"navigate(\\'dashboard\\')\" style=\"padding:8px 20px\">&#10005; Tutup</button></div>';}",
    "if(state.view!=='input-observasi'){html+='<div class=\"no-print\" style=\"margin-top:20px;text-align:right\"><button class=\"btn btn-danger\" onclick=\"navigate(\\'dashboard\\')\" style=\"padding:8px 20px\">&#10005; Tutup</button></div>';}")

# ---- 14. CSS for tabs (task spec + hover + obs-content) ----
rep(".obs-tabs{display:flex;flex-wrap:wrap;gap:4px;border-bottom:3px solid #e2e8f0;margin-bottom:0}" + NL +
    ".obs-tab{padding:12px 20px;cursor:pointer;font-weight:600;color:#64748b;border-bottom:3px solid transparent;margin-bottom:-3px;transition:all .2s;white-space:nowrap}" + NL +
    ".obs-tab.active{color:#034f1d;border-bottom-color:#034f1d;background:#f0fdf4}",
    ".obs-tabs{display:flex;flex-wrap:wrap;gap:4px;border-bottom:3px solid #034f1d;margin-bottom:20px}" + NL +
    ".obs-tab{padding:12px 20px;cursor:pointer;font-weight:600;color:#64748b;border-bottom:3px solid transparent;margin-bottom:-3px;transition:all .2s;white-space:nowrap}" + NL +
    ".obs-tab.active{color:#034f1d;border-bottom-color:#034f1d;background:#f0fdf4}" + NL +
    ".obs-tab:hover{color:#034f1d}" + NL +
    ".obs-content{padding:0}")

# ---- 15. Supervisi form last step: "Lanjut ke Kokurikuler" button ----
rep("if(isLast){nav+='<button class=\"btn btn-success\" onclick=\"saveForm()\">&#128190; Simpan</button>';}",
    "if(isLast){nav+='<button class=\"btn btn-success\" onclick=\"saveForm()\">&#128190; Simpan</button>';nav+='<button class=\"btn btn-info\" onclick=\"saveForm();setActiveTab(\\'kokurikuler\\')\" style=\"margin-left:8px\">Lanjut ke Kokurikuler \u2192</button>';}")

# ---- 16. Kokurikuler form: "Lanjut ke Ekstrakurikuler" button ----
rep("html+='<button class=\"btn btn-primary\" onclick=\"gotoObservasi(\\'kokurikuler\\')\">\u2714 Simpan</button>';",
    "html+='<button class=\"btn btn-primary\" onclick=\"gotoObservasi(\\'kokurikuler\\')\">\u2714 Simpan</button>';" + NL +
    "html+='<button class=\"btn btn-info\" onclick=\"gotoObservasi(\\'ekstrakurikuler\\')\" style=\"margin-left:8px\">Lanjut ke Ekstrakurikuler \u2192</button>';")

# ---- 17. Ekstra list edit button: keep tab ----
rep("onclick=\"state.ekstrakurikulerIdx='+i+';navigate(\\'ekstrakurikuler-form\\')\"",
    "onclick=\"state.activeTab='ekstrakurikuler';state.ekstrakurikulerIdx='+i+';navigate(\\'ekstrakurikuler-form\\')\"")

# ---- 18. addEkstrakurikuler: keep tab ----
rep("state.ekstrakurikulerIdx=data.length-1;" + NL + "navigate('ekstrakurikuler-form');",
    "state.ekstrakurikulerIdx=data.length-1;state.activeTab='ekstrakurikuler';" + NL + "navigate('ekstrakurikuler-form');")

# ---- 19. Iklim list edit button: keep tab ----
rep("onclick=\"state.iklimMadrasahIdx='+i+';navigate(\\'iklim-madrasah-form\\')\"",
    "onclick=\"state.activeTab='iklim-madrasah';state.iklimMadrasahIdx='+i+';navigate(\\'iklim-madrasah-form\\')\"")

# ---- final safety assertions ----
for bad in ["navigate('observasi')", 'data-nav="observasi"', "state.view='observasi'", "state.view!=='observasi'",
            "state.view==='observasi'", "renderObservasiPage", "setObsTab", "case 'observasi'"]:
    if bad.encode('utf-8') in data:
        print('LEFTOVER: %r still present!' % bad)
        sys.exit(1)

with open(path, 'wb') as f:
    f.write(data)
print('ALL EDITS APPLIED, file written')
