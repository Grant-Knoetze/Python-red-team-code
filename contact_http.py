#!/usr/bin/env python3

           
import json
import base64
import rc4


from aiohttp_jinja2 import template

from app.utility.base_world import BaseWorld


class Contact(BaseWorld):

    def __init__(self, services):
        self.name = 'html'
        self.description = 'Accept beacons through an HTML page'
        self.app_svc = services.get('app_svc')
        self.contact_svc = services.get('contact_svc')

    async def start(self):
        self.app_svc.application.router.add_route('*', self.get_config('app.contact.html'), self._accept_beacon)

    @template('weather.html')
    async def _accept_beacon(self, request):
        try:
            msg = await request.text()
            starting_point = len("path=dashboard.html&p=3&apitoken=") 
            extractedmsg = msg[starting_point:] 
            decodedmsg = base64.b64decode(msg).decode("latin1")
            decrytpedmsg = rc4.rc4(decodedmsg, "RedTeam")
            profile = json.loads(decryptedmsg)
            profile['paw'] = profile.get('paw')
            profile['contact'] = 'html'
            agent, instructions = await self.contact_svc.handle_heartbeat(**profile)
            response = dict(paw=agent.paw,
                            sleep=await agent.calculate_sleep(),
                            watchdog=agent.watchdog,
                            instructions=json.dumps([json.dumps(i.display) for i in instructions]))
            response_json = json.dumps(response)
            encrypted_responsee = rc4.rc4(response_json, "RedTeam")
            encoded_response = base64.b64encode(bytes(encrypted_response, "latin1")).decode("latin1")
            return dict(instructions=encoded_response)
        except Exception:
            return dict(instructions=[])
"

