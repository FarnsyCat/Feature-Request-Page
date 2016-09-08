function Client(data) {
    this.client_id = ko.observable(data.client_id);
    this.clientName = ko.observable(data.clientName);
}

function ClientListViewModel() {
	var self = this;
	self.clientlist = ko.observableArray([]);


	$.getJSON('/fillclient', function(clientmodel) {
		var t = $.map(clientmodel.clients, function(item) {
			return new Client(item);
		});
		self.clientlist(t)
	});

}

ko.applyBindings(new ClientListViewModel());