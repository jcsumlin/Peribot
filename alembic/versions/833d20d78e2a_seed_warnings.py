"""seed warnings

Revision ID: 833d20d78e2a
Revises: fd41ba413cd3
Create Date: 2019-12-31 18:23:21.573919

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision = '833d20d78e2a'
down_revision = 'fd41ba413cd3'
branch_labels = None
depends_on = None


def upgrade():
    warnings = sa.table(
        'warnings',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('server_id', sa.Integer(), nullable=False),
        sa.Column('date', sa.DateTime(), nullable=False),
        sa.Column('user_name', sa.String(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('mod_name', sa.String(), nullable=False),
        sa.Column('mod_id', sa.Integer(), nullable=False),
        sa.Column('reason', sa.String(), nullable=False),
    )
    op.bulk_insert(warnings,
        [
            {
                "id": 1,
                "date": datetime.strptime("2019-08-12", "%Y-%m-%d"),
                "server_id": "515370084538253333",
                "user_name": "May",
                "user_id": "582246286191886336",
                "mod_name": "Peridot",
                "mod_id": "464988171856510996",
                "reason": "Regarding your \"redacted\" comment in <#515371195999453185> this is just a warning to please not bring topics like that up again in here. That's very close to breaking rule 3 of the server (aka no NSFW posts at all). Please be more responsible with what you say next time. This is your first and only warning."
            },
            {
                "id": 2,
                "date": datetime.strptime("2019-08-16", "%Y-%m-%d"),
                "server_id": "448695150135345152",
                "user_name": "Clarkmiester95",
                "user_id": "166022114820882432",
                "mod_name": "J_C___",
                "mod_id": "204792579881959424",
                "reason": "youre hot"
            },
            {
                "id": 3,
                "date": datetime.strptime("2019-08-17", "%Y-%m-%d"),
                "server_id": "515370084538253333",
                "user_name": "Basil9",
                "user_id": "434881384075493376",
                "mod_name": "That One Wandering Weirdo",
                "mod_id": "303732162539159552",
                "reason": "First and last warning. Attempted mass pinging is not ok."
            },
            {
                "id": 4,
                "date": datetime.strptime("2019-09-02", "%Y-%m-%d"),
                "server_id": "515370084538253333",
                "user_name": "Reaper",
                "user_id": "131175848479817728",
                "mod_name": "J_C___",
                "mod_id": "204792579881959424",
                "reason": "please watch your language that was very rude what you said"
            },
            {
                "id": 5,
                "date": datetime.strptime("2019-09-03", "%Y-%m-%d"),
                "server_id": "515370084538253333",
                "user_name": "HeartzFenzy",
                "user_id": "558865780687634434",
                "mod_name": "Peridot",
                "mod_id": "464988171856510996",
                "reason": "Hello HeartzFenzy,\nFor the next three days you will be muted on the Cursed Pearl server due to you breaking the no spoilers rule. By changing your nickname and profile picture to the movie's main antagonist this was deemed as minor spoiler by the mod team. Please be mindful that there are many people who have not seen the movie yet and just because you have doesn't reserve you the right to act like other have also seen it. Your nickname was removed and we request to change your profile picture to something less spoilerly. Thank you and please be more careful next time."
            },
            {
                "id": 6,
                "date": datetime.strptime("2019-09-30", "%Y-%m-%d"),
                "server_id": "515370084538253333",
                "user_name": "basil",
                "user_id": "594928588424478741",
                "mod_name": "That One Wandering Weirdo",
                "mod_id": "303732162539159552",
                "reason": "For talking about NSFW subjects in the server on multiple occasions."
            },
            {
                "id": 7,
                "date": datetime.strptime("2019-09-27", "%Y-%m-%d"),
                "server_id": "515370084538253333",
                "user_name": "Marbles",
                "user_id": "479901504107446272",
                "mod_name": "That One Wandering Weirdo",
                "mod_id": "303732162539159552",
                "reason": "Stop spamming you numpty"
            },
            {
                "id": 8,
                "date": datetime.strptime("2019-06-13", "%Y-%m-%d"),
                "server_id": "515370084538253333",
                "user_name": "Hanstar",
                "user_id": "402652635569717248",
                "mod_name": "Peridot",
                "mod_id": "464988171856510996",
                "reason": "Hanster, this is the mod team. Please refrain from discussing disturbing topics in general discussion, even if it's meant as a joke. Additionally, if a moderator tells you to stop doing something please stop the first time asked. This is just a warning, but next time something of this caliber happens there will be consequences.\ngood?"
            },
            {
                "id": 9,
                "date": datetime.strptime("2019-06-13", "%Y-%m-%d"),
                "server_id": "515370084538253333",
                "user_name": "Kasai Gamma",
                "user_id": "354997736128643072",
                "mod_name": "Eldritch Horror",
                "mod_id": "254788027245789184",
                "reason": "This is the cursed pearl mod team, this is a warning for violating rule #1, despite it being well intentioned you came off as a dick and have upset several members of the server, so please refrain from doing so in the future."
            },
            {
                "id": 10,
                "date": datetime.strptime("2019-06-02", "%Y-%m-%d"),
                "server_id": "515370084538253333",
                "user_name": "ThunderFlame",
                "user_id": "224099663341551616",
                "mod_name": "Sapphire",
                "mod_id": "341067939220553728",
                "reason": "This is a formal warning: for making inappropriate jokes towards younger members in a SFW chat. Please refrain from talking about or making jokes with NSFW subject matter outside of the NSFW channels in the future as regular channels have minors in them -"
            },
            {
                "id": 11,
                "date": datetime.strptime("2019-05-28", "%Y-%m-%d"),
                "server_id": "515370084538253333",
                "user_name": "Little Fur",
                "user_id": "235075173756305408",
                "mod_name": "Eldritch Horror",
                "mod_id": "254788027245789184",
                "reason": "This is a message from the mod team, we would like to say that bringing up the leaderboard is strictly prohibited as it may cause unwanted rivalry that is not inline with the friendly environment we try to provide here, this is just a warning, but mentioning it again will result in disciplinary action."
            },
            {
                "id": 12,
                "date": datetime.strptime("2019-05-19", "%Y-%m-%d"),
                "server_id": "515370084538253333",
                "user_name": "Little Fur",
                "user_id": "235075173756305408",
                "mod_name": "Eldritch Horror",
                "mod_id": "254788027245789184",
                "reason": "This is the mod team, just reiterating what was said a little bit ago, this is simply for our logs not a separate warning for anything else."
            },
            {
                "id": 13,
                "date": datetime.strptime("2019-05-19", "%Y-%m-%d"),
                "server_id": "515370084538253333",
                "user_name": "Frankie",
                "user_id": "111608910774878208",
                "mod_name": "That One Wandering Weirdo",
                "mod_id": "303732162539159552",
                "reason": "Don't post images or chat topics with NSFW themes or subject matter in the future as it violates rule 2"
            },
            {
                "id": 14,
                "date": datetime.strptime("2019-05-18", "%Y-%m-%d"),
                "server_id": "515370084538253333",
                "user_name": "Little Fur",
                "user_id": "235075173756305408",
                "mod_name": "Peridot",
                "mod_id": "464988171856510996",
                "reason": "This is the mod team a whole warning you to stop insisting that the chat is \"dead.\" It's getting a little bit ridiculous and drives people away from talking."
            },
            {
                "id": 15,
                "date": datetime.strptime("2019-05-14", "%Y-%m-%d"),
                "server_id": "515370084538253333",
                "user_name": "thesocialz",
                "user_id": "359021000999960598",
                "mod_name": "J_C___",
                "mod_id": "204792579881959424",
                "reason": "This is a reiteration of what was addressed yesterday plus one requirement to remain active. Please do not make light of mental illness as we would like to keep this community safe and fun for all who would like to join us. The staff are requesting that you join us in a group chat for a talk regarding your recent behavior on CP and how this may affect your membership in the future."
            },
            {
                "id": 16,
                "date": datetime.strptime("2019-09-07", "%Y-%m-%d"),
                "server_id": "515370084538253333",
                "user_name": "Emma the closet girl ~",
                "user_id": "379549528405049344",
                "mod_name": "Peridot",
                "mod_id": "464988171856510996",
                "reason": "This is just a warning to reiterate what Sapphire said to you earlier. Please refrain from posting information that involves other users, this is a serious breach in privacy and above that a rule break (rule 2). This is your only warning so please do not do this again."
            },
            {
                "id": 17,
                "date": datetime.strptime("2019-09-11", "%Y-%m-%d"),
                "server_id": "515370084538253333",
                "user_name": "Plasmai",
                "user_id": "556950083384377374",
                "mod_name": "J_C___",
                "mod_id": "204792579881959424",
                "reason": "Hey there Plasmi please keep in mind our rules regarding user privacy. If you have any questions please DM a Mod. - J_C"
            },
            {
                "id": 18,
                "date": datetime.strptime("2019-09-12", "%Y-%m-%d"),
                "server_id": "606970684136226846",
                "user_name": "TheLovelyStarco",
                "user_id": "480128743466205225",
                "mod_name": "J_C___",
                "mod_id": "204792579881959424",
                "reason": "Hey this is a test"
            },
            {
                "id": 19,
                "date": datetime.strptime("2019-09-18", "%Y-%m-%d"),
                "server_id": "515370084538253333",
                "user_name": "Sapphire",
                "user_id": "341067939220553728",
                "mod_name": "J_C___",
                "mod_id": "204792579881959424",
                "reason": "https://discordapp.com/channels/515370084538253333/564316750313685002/623681362582306826"
            },
            {
                "id": 20,
                "date": datetime.strptime("2019-09-18", "%Y-%m-%d"),
                "server_id": "515370084538253333",
                "user_name": "chickenlegs",
                "user_id": "376540254745919498",
                "mod_name": "J_C___",
                "mod_id": "204792579881959424",
                "reason": "This is an official warning: Having your own political views is fine in CP but please don't use \"bait statements\" to intentionally attack the views of others. If you would like to continue to discuss any political topics in this server do so in a true debate fashion where you present your position and allow any opposition to present theirs."
            },
            {
                "id": 21,
                "date": datetime.strptime("2019-09-18", "%Y-%m-%d"),
                "server_id": "515370084538253333",
                "user_name": "0706",
                "user_id": "432353357903167500",
                "mod_name": "That One Wandering Weirdo",
                "mod_id": "303732162539159552",
                "reason": "A reminder that jokes that could be considered harassment are not appropriate in any case. Please make sure to follow rule 1 https://discordapp.com/channels/515370084538253333/515371174558040077/623866574004289536"
            }
        ]
    )


def downgrade():
    pass
