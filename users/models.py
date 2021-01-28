from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from djongo import models as MongoModels


class Scene(models.Model):
    """Model representing a scene (but not a specific copy of a scene)."""
    name = models.CharField(max_length=200, blank=False, unique=True)
    summary = models.TextField(max_length=1000)
    editors = models.ManyToManyField(User)
    creation_date = models.DateTimeField(auto_now_add=True)
    public_read = models.BooleanField(default=True)
    public_write = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.full_clean()  # performs regular validation then clean()
        super(Scene, self).save(*args, **kwargs)

    def clean(self):
        if self.name == '':
            raise ValidationError('Empty scene name!')
        self.name = self.name.strip()

    def __str__(self):
        """String for representing the scene object by name."""
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a detail record for this scene."""
        return reverse('scene-detail', args=[str(self.name)])


class ArenaObject(MongoModels.Model):
    """
    https://github.com/conix-center/arena-persist/blob/master/server.js#L26
    const arenaSchema = new mongoose.Schema({
        object_id: {type: String, required: true, index: true},
        type: {type: String, required: true, index: true},
        attributes: Object,
        expireAt: {type: Date, expires: 0},
        realm: {type: String, required: true, index: true},
        namespace: {type: String, required: true, index: true, default: 'public'},
        sceneId: {type: String, required: true, index: true},
    }, {
        timestamps: true,
    });
    """
    _id = MongoModels.ObjectIdField()
    object_id = MongoModels.CharField(max_length=200, blank=False)
    type = MongoModels.CharField(max_length=200, blank=False)
    attributes = MongoModels.JSONField()
    realm = MongoModels.CharField(max_length=200, blank=False)
    namespace = MongoModels.CharField(
        max_length=200, blank=False, default='public')
    sceneId = MongoModels.CharField(max_length=200, blank=False)
    createdAt = MongoModels.DateTimeField(auto_now_add=True)
    updatedAt = MongoModels.DateTimeField(auto_now=True)
