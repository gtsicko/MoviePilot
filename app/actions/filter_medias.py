from typing import Optional

from pydantic import Field

from app.actions import BaseAction
from app.core.config import global_vars
from app.schemas import ActionParams, ActionContext


class FilterMediasParams(ActionParams):
    """
    过滤媒体数据参数
    """
    type: Optional[str] = Field(None, description="媒体类型 (电影/电视剧)")
    category: Optional[str] = Field(None, description="媒体类别 (二级分类)")
    vote: Optional[int] = Field(0, description="评分")
    year: Optional[str] = Field(None, description="年份")


class FilterMediasAction(BaseAction):
    """
    过滤媒体数据
    """

    _medias = []

    @classmethod
    @property
    def name(cls) -> str:
        return "过滤媒体数据"

    @classmethod
    @property
    def description(cls) -> str:
        return "对媒体数据列表进行过滤"

    @classmethod
    @property
    def data(cls) -> dict:
        return FilterMediasParams().dict()

    @property
    def success(self) -> bool:
        return self.done

    def execute(self, workflow_id: int, params: dict, context: ActionContext) -> ActionContext:
        """
        过滤medias中媒体数据
        """
        params = FilterMediasParams(**params)
        for media in context.medias:
            if global_vars.is_workflow_stopped(workflow_id):
                break
            if params.type and media.type != params.type:
                continue
            if params.category and media.category != params.category:
                continue
            if params.vote and media.vote_average < params.vote:
                continue
            if params.year and media.year != params.year:
                continue
            self._medias.append(media)

        if self._medias:
            context.medias = self._medias

        self.job_done(f"过滤后剩余 {len(self._medias)} 条媒体数据")
        return context
