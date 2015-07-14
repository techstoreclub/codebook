import yaml

with open('./topics/config.yml') as f:
    site = yaml.safe_load(f)


def settings_context(_):
    return {
        'site': site
    }
