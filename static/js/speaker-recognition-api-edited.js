/*I want to thanks 'Robin Osborne' (https://github.com/rposbo), since it is only due to him arranging the code like this,
 and helped me a lot, since i understand all the code now quite clearly... and it has no requirement for an attribution but you deserve it */

function startListeningForVerification(){
	verificationProfile.profileId = 'a45424a2-26ee-4e9f-8e3a-97ce66508d80'
	navigator.getUserMedia({audio: true}, function(stream){onMediaSuccess(stream, verifyProfile, 4)}, onMediaError);
}

// 3. Take the audio and send it to the verification endpoint for the current profile Id
function verifyProfile(blob){
//	addAudioPlayer(blob);
	var verify = `${baseApi}/verify?verificationProfileId=${verificationProfile.profileId}`;
  
	var request = new XMLHttpRequest();
	request.open("POST", verify, true);
	
	request.setRequestHeader('Content-Type','application/json');
	request.setRequestHeader('Ocp-Apim-Subscription-Key', key);
  
	request.onload = function () {

		// Was it a match?
		console.log(request.responseText);		
	};
  
	request.send(blob);
}

// BurnItAll('verification') - clear verification profiles
function BurnItAll(){
	// brute force delete everything - keep retrying until it's empty
	var listing = `${baseApi}/${mode}Profiles`;

	var request = new XMLHttpRequest();
	request.open("GET", listing, true);

	request.setRequestHeader('Ocp-Apim-Subscription-Key', key);

	request.onload = function () {
		var json = JSON.parse(request.responseText);
		for(var x in json){
			if (json[x]['verificationProfileId'] == undefined) {continue;}
			var request2 = new XMLHttpRequest();
			request2.open("DELETE", listing + '/'+ json[x]['verificationProfileId'], true);
			request2.setRequestHeader('Ocp-Apim-Subscription-Key', key);
			request2.onload = function(){
				console.log(request2.responseText);
			};
			request2.send();
		}
	};

	request.send();
}

// This method adds the recorded audio to the page so you can listen to it
function addAudioPlayer(blob){	
	var url = URL.createObjectURL(blob);
	var log = document.getElementById('log');

	var audio = document.querySelector('#replay');
	if (audio != null) {audio.parentNode.removeChild(audio);}

	audio = document.createElement('audio');
	audio.setAttribute('id','replay');
	audio.setAttribute('controls','controls');

	var source = document.createElement('source');
	source.src = url;

	audio.appendChild(source);
	log.parentNode.insertBefore(audio, log);
}

// Example phrases
var thingsToRead = [
	"Never gonna give you up\nNever gonna let you down\nNever gonna run around and desert you\nNever gonna make you cry\nNever gonna say goodbye\nNever gonna tell a lie and hurt you",
	"There's a voice that keeps on calling me\n	Down the road, that's where I'll always be.\n	Every stop I make, I make a new friend,\n	Can't stay for long, just turn around and I'm gone again\n	\n	Maybe tomorrow, I'll want to settle down,\n	Until tomorrow, I'll just keep moving on.\n	\n	Down this road that never seems to end,\n	Where new adventure lies just around the bend.\n	So if you want to join me for a while,\n	Just grab your hat, come travel light, that's hobo style.",
	"They're the world's most fearsome fighting team \n	They're heroes in a half-shell and they're green\n	When the evil Shredder attacks\n	These Turtle boys don't cut him no slack! \n	Teenage Mutant Ninja Turtles\nTeenage Mutant Ninja Turtles",
	"If you're seein' things runnin' thru your head \n	Who can you call (ghostbusters)\n	An' invisible man sleepin' in your bed \n	Oh who ya gonna call (ghostbusters) \nI ain't afraid a no ghost \n	I ain't afraid a no ghost \n	Who ya gonna call (ghostbusters) \n	If you're all alone pick up the phone \n	An call (ghostbusters)",
];

// Get the Cognitive Services key from the querystring
var key = '8763cd74d31646068f11f8a7e342f42b' ;
var baseApi = 'https://westus.api.cognitive.microsoft.com/spid/v1.0';

// Speaker Recognition API profile configuration - constructs to make management easier
var Profile = class { constructor (name, profileId) { this.name = name; this.profileId = profileId;}};
var VerificationProfile = class { constructor (name, profileId) { this.name = name; this.profileId = profileId; this.remainingEnrollments = 3}};
var profileIds = [];
var verificationProfile = new VerificationProfile();


(function () {
	// Cross browser sound recording using the web audio API
	navigator.getUserMedia = ( navigator.getUserMedia ||
							navigator.webkitGetUserMedia ||
							navigator.mozGetUserMedia ||
							navigator.msGetUserMedia);

	// Really easy way to dump the console logs to the page
	var old = console.log;
	var logger = document.getElementById('log');
	var isScrolledToBottom = logger.scrollHeight - logger.clientHeight <= logger.scrollTop + 1;
    
	console.log = function () {
		for (var i = 0; i < arguments.length; i++) {
			if (typeof arguments[i] == 'object') {
				logger.innerHTML += (JSON && JSON.stringify ? JSON.stringify(arguments[i], undefined, 2) : arguments[i]) + '<br />';
			} else {
				logger.innerHTML += arguments[i] + '<br />';
			}
			if(isScrolledToBottom) logger.scrollTop = logger.scrollHeight - logger.clientHeight;
		}
		old(...arguments);
	}
	console.error = console.log; 
})();
