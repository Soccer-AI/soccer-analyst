class ObjectTracking(object):
    def __init__(self, tracker, config):
        self.results = []
        self.tracker = tracker
        self.config = config

    def update(self, frame_id, output_results, img_info, img_size):
        online_targets = self.tracker.update(output_results, img_info, img_size)
        online_tlwhs = []
        online_ids = []
        online_scores = []
        for t in online_targets:
            tlwh = t.tlwh
            tid = t.track_id
            vertical = tlwh[2] / tlwh[3] > self.config.aspect_ratio_thresh
            if tlwh[2] * tlwh[3] > self.config.min_box_area and not vertical:
                online_tlwhs.append(tlwh)
                online_ids.append(tid)
                online_scores.append(t.score)
                self.results.append(
                    f"{frame_id},{tid},{tlwh[0]:.2f},{tlwh[1]:.2f}," +
                    f"{tlwh[2]:.2f},{tlwh[3]:.2f},{t.score:.2f},-1,-1,-1\n"
                )
        return online_tlwhs, online_ids, online_scores
