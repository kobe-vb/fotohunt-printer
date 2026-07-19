import random

from models.models import TaskRecord

LOCATIONS: list[tuple[str, int]] = [
    ("eetent, 1"),
    ("leiderstent", 3),
    ("hoek", 1),
    ("bagage", 1),
    ("hout hokje", 1),
    ("in de rievier", 5),
    ("wc", 1),
    ("grasveld", 1),
    ("balke container", 1) 
]

POSES: list[tuple[str, int]] = [
    ("zittend op de grond", 1),
    ("vleeshoop", 3),
    ("piramide", 2),
    ("op elkaars knie zitten maar dan op ne rechte lijn", 1),
    ("steretje maken", 1),
    ("fack you ", 1),
    ("alemaal springent", 3),
    ("super man", 1),
    ("een fiets na doen", 2),
    ("halft benen open andere halt onder de benen met zo hunne kop", 1),
    ("vrij spel wees cratief", 5),
    ("dooie vis", 4),
    ("foto 1", 3),
    ("foto 2", 1),
    ("foto 3", 1),
    ("foto 4", 1),
    ("foto 5", 2),
    ("foto 6", 1),
    ("foto 7", 1),
    ("foto 8", 1),
    ("foto 9", 2),    
    ("foto 10", 1),    
    ("foto 11", 1),
    ("foto 12", 1),
    ("foto 13", 1),
    ("foto 14", 4),
    ("foto 15", 1),
    ("foto 16", 1),
    ("foto 17", 3),
    ("foto 18", 1),
    ("foto 19", 2),
    ("foto 20", 2)
] 

OBJECTS: list[tuple[str, int]] = [
    ("een flesje water", 1),
    ("een rugzak", 1),
    ("tent paal", 2),
    ("ronde steen", 4),
    ("pollepel", 2),
    ("pikket", 2),
    ("grondboor", 2),
    ("ducktape op mond", 3),
    ("lege water fles", 1),
    ("klijn blikje ictea", 4),
    ("wc rol", 4),
    ("mooie kartone doos rubiqscube", 3),
    ("lepel", 1),
    ("bank", 4),
    ("gele hoed", 2),
    ("pinpong bal", 2),
    ("bije pet", 2),
]

EXTRAS: list[tuple[str, int]] = [
    ("tafel", 3),
    ("andere mans dan onze tak", 2),
    ("iedereen rug naar foto", 2),
    ("iemand liggen op de grond", 1),
    ("iedereen tong uit steken", 1),
    ("bolderkar", 2),
    ("1 iemand zit in tent zak", 2),
    ("jongesn mijsjesn swap kleren", 3),
    ("in kleur american vlag blouw rood wit", 3),
    ("balauwe balk", 2),
    ("met vogel", 3),
    ("1 iemand ondersteboven", 1),
    ("1 iemand in de lucht", 1),
    ("met levend dier", 1),
    ("met deur", 2),
    ("1 tje op de rug van iemand anders", 2),
    
    ("burgeking donut", 4),
    ("bernaar", 6),
    ("desie", 8),
    ("staf de jiraf", 7),
    ("ana frank", 5),
    ("fluo vestje", 4),
    ("voedbal", 4),
    ("cowboy hoed", 7),
    ("hammer", 6),
    ("coole tak", 8),
    ("beleblaas", 10)
]

SPECIAL_TASKS: list[tuple[str, int]] = [
    ("allen in houten kisten", 11),
    ("allen gezichten boven haag", 7),
    ("allen hangen aan de voedbal gool", 10),
    ("iedereen t-shirt achterstevoren", 8),
    ("mooimakers foto", 15),
    ("knuffel allemaal ne boom", 12)
]

NORMAL_VS_SPECIAL_SPLIT = 0.8 

class TaskGenerator:

    def genereer_normale_taak(
        self, team_id: str, sequence_number: int, extra_count: int = 0
    ) -> TaskRecord:
        location_text, location_likes = random.choice(LOCATIONS)
        pose_text, pose_likes = random.choice(POSES)
        object_text, object_likes = random.choice(OBJECTS)

        record = TaskRecord(
            team_id=team_id,
            sequence_number=sequence_number,
            location_text=location_text,
            location_likes=location_likes,
            pose_text=pose_text,
            pose_likes=pose_likes,
            object_text=object_text,
            object_likes=object_likes,
        )
        self._voeg_extras_toe(record, extra_count)
        return record

    def genereer_speciale_taak(
        self, team_id: str, sequence_number: int, extra_count: int = 0
    ) -> TaskRecord:
        special_task_text, special_task_likes = random.choice(SPECIAL_TASKS)
        return self.genereer_specifieke_taak(
            team_id, sequence_number, special_task_text, special_task_likes, extra_count
        )

    def genereer_specifieke_taak(
        self,
        team_id: str,
        sequence_number: int,
        special_task_text: str,
        special_task_likes: int,
        extra_count: int = 0,
    ) -> TaskRecord:
        record = TaskRecord(
            team_id=team_id,
            sequence_number=sequence_number,
            special_task_text=special_task_text,
            special_task_likes=special_task_likes,
        )
        self._voeg_extras_toe(record, extra_count)
        return record

    def genereer_taak(
        self, team_id: str, sequence_number: int, extra_count: int = 0
    ) -> TaskRecord:
        if random.random() < NORMAL_VS_SPECIAL_SPLIT:
            return self.genereer_normale_taak(team_id, sequence_number, extra_count)
        return self.genereer_speciale_taak(team_id, sequence_number, extra_count)

    def _voeg_extras_toe(self, record: TaskRecord, extra_count: int) -> None:

        total = min(5, extra_count)
        #TODO
        total = 5
        if total > 0:
            chosen = random.sample(EXTRAS, k=total)
            record.set_extras([{"text": text, "likes": likes} for text, likes in chosen])


task_generator = TaskGenerator()