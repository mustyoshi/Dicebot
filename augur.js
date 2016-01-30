var Skyweb = require('../skyweb');
var username = process.argv[2];
var password = process.argv[3];
var diceMatch = /(\d+)d(\d*)([k]?)(\d+)([-+]?)(\d*)/igm;
if(!username || !password) {
	throw new Error('Username and password should be provided as commandline arguments!');
}
var skyweb = new Skyweb();
skyweb.login(username, password).then(function(skypeAccount) {
	console.log('Skyweb is initialized now');
});
function s1() {

}

skyweb.messagesCallback = function(messages) {
	messages.forEach(function(message) {
		console.log(message.resource.messagetype);
		var targ = /\<target\>(\d):(.+)\<\/target\>/;
		var conversationLink = message.resource.conversationLink;
		var conversationId = conversationLink.substring(conversationLink.lastIndexOf('/') + 1);
		if(message.resource.messagetype == "ThreadActivity/DeleteMember") {
			var result = targ.exec(str);
			if(result != null) {
				skyweb.sendMessage(conversationId, "RIP in peace " + result[2]);
			}

		}
		if(message.resource.messagetype == "ThreadActivity/AddMember") {
			var result = targ.exec(str);
			if(result != null) {
				skyweb.sendMessage(conversationId, "Hello " + result[2]);
			}

		}
		if(message.resource.from.indexOf(username) === -1 && message.resource.messagetype == "RichText" || message.resource.messagetype == "Text" && message.resource.content != null) {

			if(message.resource.content.indexOf("<legacyquote>") === -1) {
				if(message.resource.content.indexOf("gf") != -1 && Math.random() <= .01) {
					skyweb.sendMessage(conversationId, "tfw no robot gf");
				}
				if(message.resource.content.indexOf("check em") != -1 || message.resource.content.indexOf("checkem") != -1 || message.resource.content.indexOf("reroll") != -1 || message.resource.content.indexOf("if dubs") != -1) {
					var t = String(parseInt(Math.random() * 1000000));
					var resp = message.resource.imdisplayname + " rolled " + t;
					var s = t[t.length - 1];
					var d = 1;
					for(var i = t.length - 2; t > 0; i--) {
						if(s == t[i]) {
							d++;
						} else {
							break;
						}
					}
					switch(d) {
						case 2:
							resp += "\nCheck Em!";
							break;
						case 3:
							if(s == "6") {
								resp += "\nDemonic Trips!";
							} else {
								resp += "\nTrips!";
							}
							break;
						case 4:
							resp += "\nYou're a supreme bean!";
							break;
						case 5:
							resp += "\nUnreal check em\n";
							break;

					}

					skyweb.sendMessage(conversationId, resp);

				} else
					switch(message.resource.content) {
						/*case "lose yourself":
						 var resp = "Look, if you had, one shot\nOr one spaghetti, to seize every spaghetti you ever wanted\nIn one moment\nWould capture it, or just let it slip?";
						 skyweb.sendMessage(conversationId,resp);
						 break;*/
						case "deez":
							skyweb.sendMessage(conversationId, "nutz");
							break;
						case "help":
							skyweb.sendMessage(conversationId, "1d20 rolls a 20 sided die.\n4d6k3 rolls 4 six sided die and keeps highest 3\n1d20+3 adds 3 to a 20 roll, works for subtraction too\nSend problems to Skype:mustyoshi or dice@mustyoshi.com.");
							break;
						default:

							var diceMatch = /(\d+)d(\d*)([k]?)(\d+)([-+]?)(\d*)/igm;
							var str = message.resource.content;
							var resp = "";

							var result = diceMatch.exec(str);
							if(result != null)
							/*while(diceMatch.test(str))*/
							{

								if(message.resource.imdisplayname == "mustyoshi") {
									console.log(JSON.stringify(message));
									//resp += JSON.stringify(message) + "\n";
								}
								//str = str.substring(str.indexOf(result[0]) + result[0].length);
								var numDice = parseInt(result[1]);
								var nSides = result[2];
								if(result[3] == "") {
									nSides += result[4];
								}
								var nSides = parseInt(nSides);
								//resp += "Got " + numDice + " x " + nSides;
								var tot = 0;
								var rolls = [];
								for(var i = 0; i < Math.min(numDice, 100); i++) {
									var rol = parseInt(Math.random() * Math.min(nSides, 1000000000)) + 1;
									tot += rol;
									rolls.push(rol);
								}
								if(result[3] != ""){
									rolls.sort();
									//rolls.reverse();
									for(var i=0;i<Math.max(0, numDice - result[4]);i++){
										rolls[i] = rolls[i]*-1;
										tot += rolls[i];
									}
								}
								if(result[5] != "") {
									if(result[5] == "+")
										tot += parseInt(result[6]);
									else
										tot -= parseInt(result[6]);
								}
								resp += message.resource.imdisplayname + " rolled " + result[0] + " " + JSON.stringify(rolls) + result[5] + result[6] + " = " + tot;

							}

							if(resp.length > 0)
								skyweb.sendMessage(conversationId, resp);

							//}

							break;
					}
			}
		}
	});
};
//# sourceMappingURL=demo.js.map