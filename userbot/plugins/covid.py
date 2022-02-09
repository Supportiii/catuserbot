# corona virus stats for catuserbot
from covid import Covid

from . import catub, covidindia, edit_delete, edit_or_reply

plugin_category = "extra"


@catub.cat_cmd(
    pattern="covid(?:\s|$)([\s\S]*)",
    command=("covid", plugin_category),
    info={
        "header": "To get latest information about covid-19.",
        "description": "Get information about covid-19 data in the given country/state(only Indian States).",
        "usage": "{tr}covid <state_name/country_name>",
        "examples": ["{tr}covid andhra pradesh", "{tr}covid india", "{tr}covid world"],
    },
)
async def corona(event):
    "To get latest information about covid-19."
    input_str = event.pattern_match.group(1)
    country = (input_str).title() if input_str else "World"
    catevent = await edit_or_reply(event, "`Collecting data...`")
    covid = Covid(source="worldometers")
    try:
        country_data = covid.get_status_by_country_name(country)
    except ValueError:
        country_data = ""
    if country_data:
        hmm1 = country_data["confirmed"] + country_data["new_cases"]
        hmm2 = country_data["deaths"] + country_data["new_deaths"]
        data = ""
        data += f"\n⚠️ Bestätigt   : <code>{hmm1}</code>"
        data += f"\n😔 Aktiv           : <code>{country_data['active']}</code>"
        data += f"\n⚰️ Tote         : <code>{hmm2}</code>"
        data += f"\n🤕 Kranke          : <code>{country_data['critical']}</code>"
        data += f"\n😊 Genesene   : <code>{country_data['recovered']}</code>"
        data += f"\n💉 Tests (gesamt)    : <code>{country_data['total_tests']}</code>"
        data += f"\n🥺 Neue Fällt   : <code>{country_data['new_cases']}</code>"
        data += f"\n😟 Neue Tote : <code>{country_data['new_deaths']}</code>"
        await catevent.edit(
            "<b>Corona Virus Info von {}:\n{}</b>".format(country, data),
            parse_mode="html",
        )
    else:
        data = await covidindia(country)
        if data:
            cat1 = int(data["new_positive"]) - int(data["positive"])
            cat2 = int(data["new_death"]) - int(data["death"])
            cat3 = int(data["new_cured"]) - int(data["cured"])
            result = f"<b>Corona virus info of {data['state_name']}\
                \n\n⚠️ Bestätigt   : <code>{data['new_positive']}</code>\
                \n😔 Aktiv           : <code>{data['new_active']}</code>\
                \n⚰️ Tote         : <code>{data['new_death']}</code>\
                \n😊 Genesene   : <code>{data['new_cured']}</code>\
                \n🥺 Neue Fälle   : <code>{cat1}</code>\
                \n😟 Neue Tote : <code>{cat2}</code>\
                \n😃 Neue geheilte  : <code>{cat3}</code> </b>"
            await catevent.edit(result, parse_mode="html")
        else:
            await edit_delete(
                catevent,
                "`Corona Virus Info of {} is not avaiable or unable to fetch`".format(
                    country
                ),
                5,
            )
