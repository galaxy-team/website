var console;
var document;
var $;
var window;
// var setInterval;
var interval_id;

$(document).ready(function(){
    "use strict";

    function build_events(event_info){
        // console.log(event_info);
        var valid_events = [
            'PushEvent',
            'CreateEvent',
            'DeleteEvent',
            'PullRequestEvent'
        ];

        var sentence_templates = {
            'PushEvent': 'Pushed to ',
            'CreateEvent': (
                'Created a new {{>ref_type}}; '),
            'DeleteEvent': (
                'Deleted a {{>ref_type}} on repository '),
            'PullRequestEvent': '{{>action}} a pull request on '
        };

        $.templates(sentence_templates);

        if (sentence_templates[event_info.type] === undefined)
            return null;

        event_info.invoker = event_info.actor.login;
        event_info.repository = event_info.repo.name;
        if (event_info.payload.hasOwnProperty('ref_type'))
            event_info.ref_type = event_info.payload.ref_type;

        event_info.avatar_url = event_info.actor.avatar_url;

        if (event_info.payload.hasOwnProperty('action'))
            event_info.action = event_info.payload.action;


        // only seems to work if i call it once before
        $.render[event_info.type](event_info);

        var string = $.render[event_info.type](event_info);

        var end = {
            'string': string,
            'info': event_info
        };

        return end;
    }

    function get_repo_events(repos){

        var process = function(data){
            var all_events = [];
            console.log('Request returned');
            for (var q=0;q<data.length;q++){
                all_events.push(data.data[q]);
            }
            return all_events;
        };

        var fetches = [];

        var dff = $.Deferred();
        for (var i=0;i<repos.length;i++){
            fetches.push($.getJSON(
                'https://api.github.com/repos/' + repos[i].full_name + '/events?callback=?',
                process));
        }

        fetches = $.when.apply($, fetches).promise();
        fetches.done(function(){
            var all_events = [];
            for (var r=0;r<arguments.length;r++){
                for (var e=0;e<arguments[r][0].data.length;e++){
                    all_events.push(arguments[r][0].data[e]);
                }
            }
            dff.resolve(all_events);
        });

        return dff.promise();
    }

    function refresh_events(data){
        $('.h-feed').html(
            $("#eventTemplate").render(data)
        );
    }


    function get_events(repos){
        var dff = $.Deferred();

        get_repo_events(repos).done(function(all_events){
            console.log(all_events.length + ' events');

            for (var i=0;i<all_events.length;i++){
                var timetuple = /(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})Z/.exec(all_events[i].created_at);
                timetuple = timetuple.slice(1, 7);

                var unix_time = new Date(
                    timetuple[0],
                    timetuple[1],
                    timetuple[2],
                    timetuple[3],
                    timetuple[4],
                    timetuple[5]);

                all_events[i].created_at = unix_time.getTime();
            }

            all_events = all_events.sort(function(x, y){return y.created_at - x.created_at;});

            var end_events = [];
            for (var q=0;q<all_events.length;q++){
                var event_dict = build_events(all_events[q]);
                if (event_dict){
                    end_events.push(event_dict);
                }
            }

            dff.resolve(end_events);
        });

        return dff.promise();
    }

    // setup
    console.log('Setting up github event stream...');

    $.getJSON('https://api.github.com/orgs/galaxy-team/repos?callback=?', function(d){
        if (d.data.message !== undefined){
            if ((d.data.message).substring(0, 23) === "API Rate Limit Exceeded"){
                throw new Error('API Limit reached');
            } else {
                console.log("Message; " + d.data.message);
            }
        }
        var repos = d.data;

        var repo_names = [];
        for(var z=0;z<repos.length;z++){
            repo_names.push(repos[z].full_name);
        }

        console.log(repo_names);

        function update_events(repos){
            var dff = $.Deferred();
            get_events(repos).done(function(result){
                console.log('Setup finished');
                refresh_events(result);
                dff.resolve();
            });
            return dff.promise();
        }

        update_events(repos).done(function(){
            console.log('First iteration successful. Commencing execute on interval.');
            interval_id = window.setInterval(update_events, 5 * 60 * 1000, repos);
        });
    });
});
