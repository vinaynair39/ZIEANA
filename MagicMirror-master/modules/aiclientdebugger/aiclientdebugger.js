//aiclientdebugger.js

Module.register("aiclientdebugger",{

	// Default module config.
	defaults: {
		animationSpeed: 0.2 * 1000
	},

	// Define required translations.
	getTranslations: function() {
		// The translations for the defaut modules are defined in the core translation files.
		// Therefor we can just return false. Otherwise we should have returned a dictionairy.
		// If you're trying to build your own module including translations, check out the documentation.
		return false;
	},

	// Define start sequence.
	start: function() {
		Log.log("Starting module: " + this.name);

		this.sendSocketNotification("INITIALIZE", {})
		
	},

	// Override dom generator.
	getDom: function() {
		var wrapper = document.createElement("div");
		if (this.microphoneEnabled) {
			wrapper.innerHTML = "<img src=\"" + this.file("microphone.png") + "\" style=\"width:30px;height:30px;\">"
			wrapper.innerHTML += "I'm listening";
			wrapper.className = "small bright";


		}
		else if (this.Found_audioPresent){
		    wrapper.innerHTML = "<img src=\"" + this.file("audio.png") + "\" style=\"width:30px;height:30px;\">"
		    wrapper.innerHTML += "Audio Found";
			wrapper.className = "small bright";
		}


		return wrapper
	},

	// Override socket notification handler.
	socketNotificationReceived: function(notification, payload) {
		console.log("module received: " + notification)
		var self = this

		if (notification == "MICROPHONE"){
			this.microphoneEnabled = payload.enabled
			this.updateDom(this.config.animationSpeed);
		}

		else if (notification == "Found_audio"){
		    this.Found_audioPresent = "Found_audio"
			this.updateDom(this.config.animationSpeed);
			}
	}
});
