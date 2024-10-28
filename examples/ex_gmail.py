from gmail import Gmail
from agent import AgentMail


def main():
    # create template (prompt)
    template = """Tu es un expert en classification de mails pour une société de gestion locative.
    Ta seule tâche est de déterminer si un mail est une demande d'intervention ou non.

    Voici des exemples de demandes d'intervention :

    EXEMPLE 1:
    Mail: Bonjour,
    Depuis plusieurs jours ma porte est très compliquée à fermer de l'extérieur et aujourd'hui après 15 minutes à essayer de la fermer elle ne s'est toujours pas fermée, mon voisin m'a dit qu'il avait eu le même problème et avait donc fait changer la serrure.
    Est-il possible de faire venir un serrurier ?
    Merci d'avance pour votre réponse 
    Martin Bollen
    Classification: OUI (demande explicite d'intervention d'un serrurier)

    EXEMPLE 2:
    Mail: Bonjour, 
    Depuis mon arrivée, la peinture se dégrade, se décroche autour du chambranle dans les toilettes, la salle de bain, le mur adjacent dans le salon. 
    Je vous demande de bien vouloir faire une visite afin de corriger ce défaut, qui n'est pas de l'entretien mais de la responsabilité du propriétaire dans la mise en œuvre de l'application des peintures.
    Par ailleurs, il a été constaté depuis plusieurs hivers une humidité importante dans la chambre entrainant l'apparition de champignons sur l'ensemble des murs de la pièce, malgré une aération régulière et la mise en place de déshumidificateurs.
    Je reste à votre disposition pour convenir d'un rendez-vous sur place.
    Charle CLAP
    Classification: OUI (demande de visite pour réparation peinture et problème d'humidité)

    Mail à analyser :
    {mail_content}

    Réponds uniquement avec un JSON contenant :
    - is_intervention (boolean)
    - raison (string court expliquant pourquoi)
    """

    # init agent
    agentMail = AgentMail(template=template)

    # init Gmail tools
    gmail = Gmail()

    # get mails
    emails = gmail.getMail(max_results=1)

    for email in emails:
        print(f"\nSujet: {email['subject']}")
        print(f"De: {email['sender']}")
        print(f"Date: {email['date']}")
        print("Corps du message:", email['body'][:100], "...")

        # check each mail
        data = agentMail.classifyMail(email['body'])

        if data.is_intervention:
            body = """Bonjour,\n\nNous avons bien reçu votre demande et nous vous informons que nous mettons tout en œuvre pour trouver une solution rapide. Afin de traiter votre demande au plus vite ou de dépêcher un professionnel qualifié si nécessaire, merci de bien vouloir compléter le formulaire suivant : https://sinitre.mon-site.fr/ \n\nCordialement,\n\nVotre équipe de gestion"""

            # send mail
            gmail.sendMail(to=email['sender'], subject="NOREPLY: SINISTRE", body=body)


if __name__ == '__main__':
    main()