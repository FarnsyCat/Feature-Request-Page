function HeaderViewModel() {
    //this.currentUserName = ko.observable('<%=HttpContext.Current.Session["username"]%>');
    //this.currentUserID = ko.observable('<%=HttpContext.Current.Session["userid"]%>');
    //this.currentUserRole = ko.observable("Session['userrole']");
    //this.isadmin = ko.observable("hidden");
}
    ko.applyBindings(new HeaderViewModel(), document.getElementById('ViewHeader'));
