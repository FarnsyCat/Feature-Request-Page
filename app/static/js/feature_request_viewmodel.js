function Client(data) {
    this.client_id = ko.observable(data.client_id);
    this.clientName = ko.observable(data.clientName);
}

function Product(data) {
    this.product_id = ko.observable(data.product_id);
    this.productName = ko.observable(data.productName);
}

function Priority(data) {
    this.priority = ko.observable(data);
}

function FeatureRequestViewModel() {
    var self = this;

    self.selectedChoice = ko.observable();
    self.prioritylist = ko.observableArray([]);
    self.clientlist = ko.observableArray([]);
    self.productlist = ko.observableArray([]);
    this.optionsCaptionClient = ko.observable('-- select an option --');
    this.optionsCaptionPriority = ko.observable('-- select an option --');
    this.optionsCaptionProduct = ko.observable('-- select an option --');
    var data = {
        client_id: this.selectedChoice
    };


    self.selectionChanged = function () {
        $.post("/fillfeaturerequest", data, function (returnedData) {
            self.prioritylist.removeAll();
            for (var i = 1; i <= returnedData.priority; i++) {
                p = new Priority(i)
                self.prioritylist.push(p);
            }
        });
    };


    $.getJSON('/fillfeaturerequest', function (featuremodel) {
        var c = $.map(featuremodel.clients, function (item) {
            return new Client(item);
        });
        self.clientlist(c)
        var p = $.map(featuremodel.products, function (item) {
            return new Product(item);
        });
        self.productlist(p)
    });
}
ko.applyBindings(new FeatureRequestViewModel(), document.getElementById('ViewFeatureRequest'));
