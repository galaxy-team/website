var build_html;

$(document).ready(function(){
    function get_repo_events(repos){
        all_events = [];
        for (var i=0;i<repos.length;i++){
            events = $.ajax('https://api.github.com/repos/' + repos[i].full_name + '/events');
            for (var q=0;q<events.length;q++){
                all_events.push(events[q]);
            }
        }
        return all_events;
    }


    function build_events(event_info){
        valid_events = [
            'PushEvent',
            'CreateEvent',
            'DeleteEvent',
            'PullRequestEvent'
        ];

        sentence_templates = {
            'PushEvent': 'Pushed to ',
            'CreateEvent': (
                'Created a new {ref_type}; '),
            'DeleteEvent': (
                'Deleted a {ref_type} on repository '),
            'PullRequestEvent': '{action} a pull request on '
        };

        if (!valid_events.indexOf(event_info.type))
            return null;

        event_info.invoker = event_info.actor.login;
        event_info.repository = event_info.repo.name;
        if (event_info.payload.indexOf('ref_type'))
            event_info.ref_type = event_info.payload.ref_type;

        if (event_info.payload.indexOf('action'))
            event_info.action = event_info.payload.action;

        string = sentence_templates[event_info.type].format(event_info);

        end = {
            'string': string,
            'info': event_info
        };

        return end;
    }


    build_html = function (){
        $.getJSON('/stream', function(data){
            console.log('Got data :D');
            console.log(data);
            // Render the template with the event data and insert
            // the rendered HTML under the "movieList" element
            $('.h-feed').html(
                $("#eventTemplate").render(data)
            );
        });
    };

    build_html();

    // def get_events():
    //     end_events = []
    //     all_events = list(get_repo_events(repos.json()))
    //     for event in all_events:
    //         parsed_date = datetime.datetime.strptime(event['created_at'], "%Y-%m-%dT%H:%M:%SZ")
    //         unix_time = time.mktime(parsed_date.timetuple())
    //         event['created_at'] = unix_time

    //     all_events = sorted(all_events, key=lambda x: x['created_at'])[::-1]

    //     for event in all_events:
    //         event_dict = build_events(event)
    //         if event_dict:
    //             end_events.append(event_dict)
    //     return end_events


    // console.log('INFO; '+'Setting up github event stream...')

    // # with open('debug.json', 'r') as fh:
    // #     repo_events = json.load(fh)

    // # setup
    // repos = authed_fetch('https://api.github.com/orgs/galaxy-team/repos')

    // console.log('INFO; '+', '.join([repo['full_name'] for repo in repos.json()]))

    // # repo_events = list(
    // #     get_repo_events(repos.json()))
    // # with open('debug.json', 'w') as fh:
    // #     json.dump(list(repo_events), fh)

    // console.log('INFO; '+'Setup finished')

});



