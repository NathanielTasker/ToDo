function openWin(){
    tran_edit = window.open("{% url 'tasks:edit' task.id %}", "tran_edit", "width=640, height=400, scrollbars=no, status=no, toolbar=no, location=no, menubar=no, directories=no, resizable=yes");
    tran_edit.focus();
}