from semantic_router import Route
import os
from semantic_router.encoders import CohereEncoder, OpenAIEncoder
from semantic_router.layer import RouteLayer

# for Cohere

def choice(message):
    os.environ["COHERE_API_KEY"] = "pcDhbgUFdCO7rSCkXFAB0Urv6uN4cye3IUaztOd1"
    encoder = CohereEncoder()


    gfq = Route(
        name="general finance question",
        utterances=[
    "c'est quoi une action ?",
    "c est quoi un actif ?",
    "c'est quoi un indice de TUNIDEX ?",
    "expliquer le Terme OPVCM ?",
    "de quoi consiste l'analyse financiere ?",
    "Qu'est-ce qu'un marché?",
    "de quoi consiste la négociation ?",
    "c'est quoi le cours theorique du droit d'attribution ?",
    "expliquer la composition de l'indice TUNIDEX ?",
    "quelle est le role de banque centrale ?",
    "quelle sont les differents types d'actifs ?",
    "quelle est la difference entre indice TUNIDEX et les INDICE Sectoriels ?",
    "donner moi les different types des banques ?",
    "quelle est la difference entre l'indice alpha et l'indice beta ?",
    "quelles est la relation entre action ,actionnaire et appel d'offre?",
    "quelles sont les differents type de marché ?",
    "expliquer les differnets types d'actions détenues ?",
    "quelles sont les different types de cours theorique du droit ?",
    "quelles sont les different types de taux ?",
    "expliquer la composition de l'indice TUNIDEX ?",
    "quelle est la plateforme lancé en 1997 et géeréé par la Deutshe Borese ?",
    "Qu'est-ce qui s'est passé en 1964 pour faciliter l'accés des particuliers aux marché boursiers ?",
    "est ce que le Pré-ouverture de la bourse de Paris est entre 7h15 et 9h00?",
    "Quel est le nom du plan que le gouvernement américain a décidé de mettre en place pour faire face à la crise ?",
    "La répartition du capital s'organise avec au moins 60% d'actifs immobiliers et 10% de liquidités. Quel est l'organisme qui utilise cette politique ?",
    "quelle est La nomenclature sectorielle que les indices sectoriels suivent ?",
    "que represente la formule suivante: Ds=(N/(A+N))*(C-PE-D) ?",
    "les seuils qui suivent ceux de la ligne principale, et le prix de référence de la nouvelle action souscrite est égal à : Ns = C - D de quoi je suis entrain de parler ?",
    "En quelle année Henry Varnum Poor a-t-il commencé à fournir des informations financières aux investisseurs ?",
    "Quel est le nom de l'indice qui mesure la performance des 115 valeurs boursières continues de la Place de Madrid et en quelle année a-t-il commencé ?",
        ],
    )
    FORTES = Route(
        name="FORTES",
        utterances=[
            "Let's compare the top gainers and losers today. Are there any industries with a strong presence on both lists?",
            "How do the percentage changes of the top gainers stack up against the biggest losers?",
            "Is there any overlap between companies on today's movers list and those on the list from yesterday?",
            "Out of the top gainers and losers, can you highlight any companies that fit my investment criteria (e.g., sector, market cap)?",
            "Considering both gainers and losers, are there any companies that have been in the news recently?",
            "Based on the trends in gainers and losers, which sectors might be outperforming or underperforming the overall market?",
            "Are there any major news events that might explain the movement of stocks on both the gainers and losers lists?",
            "For companies on both the gainers and losers lists, is there any analyst rating changes that might be influencing their movement?",
        ],
    )

    routes = [gfq, FORTES]

    rl = RouteLayer(encoder=encoder, routes=routes)
    out = rl(message)
    return out.name
