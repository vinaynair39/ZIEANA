//node_helper.js

var NodeHelper = require("node_helper");

module.exports = NodeHelper.create({
	// Subclass start method.
	start: function() {
		var self = this;
		var events = [];

		this.fetchers = [];

		console.log("Starting node helper for: " + this.name);

	    this.expressApp.get('/microphone', function (req, res) {
	    	if (req.query.enabled.toLowerCase() == "true") {
	    		self.sendSocketNotification("MICROPHONE", {"enabled":true})
	    	} else if (req.query.enabled.toLowerCase() == "false") {
	    		self.sendSocketNotification("MICROPHONE", {"enabled":false})
	    	} else {
	    		res.sendStatus(400)
	    		return
	    	}

	        res.sendStatus(200);
	    });

	    this.expressApp.get('/Found_audio', function (req, res) {
	       if (req.query.present.toLowerCase() == "true") {
	    		self.sendSocketNotification("Found_audio", {"present":true})
	    	} else if (req.query.present.toLowerCase() == "false") {
	    		self.sendSocketNotification("Found_audio", {"present":false})
	    	} else {
	    		res.sendStatus(400)
	    		return
	    	}

	        res.sendStatus(200);
	    });
	},

	// Subclass socketNotificationReceived received.
	socketNotificationReceived: function(notification, payload) {
		console.log("helper received: " + notification)
	}
})