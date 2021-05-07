import json

from django.core.serializers.json import DjangoJSONEncoder
from django.views.generic.base import TemplateView


class GraphQLPlaygroundView(TemplateView):
    template_name = "playground.html"

    endpoint: str = None
    subscription_endpoint: str = None
    workspace_name: str = None
    config: dict = None
    settings: dict = None

    def __init__(
        self,
        endpoint: str = None,
        subscription_endpoint: str = None,
        workspace_name: str = None,
        config: dict = None,
        settings: dict = None,
        **kwargs
    ):
        super(GraphQLPlaygroundView, self).__init__(**kwargs)
        self.options = {
            "endpoint": endpoint,
            "subscriptionEndpoint": subscription_endpoint,
            "workspaceName": workspace_name,
            "config": config,
            "settings": settings,
        }

    def get_context_data(self, **kwargs):
        context = super(GraphQLPlaygroundView, self).get_context_data(**kwargs)
        context["options"] = json.dumps(self.options, cls=DjangoJSONEncoder)
        return context
